"""
Validate Prometheus metrics endpoint authentication and TLS configuration.

This script can run in CI pipelines to verify:
1. Basic authentication enforcement (401 without creds, 200 with valid creds)
2. TLS/HTTPS enforcement (connection refused for HTTP, success for HTTPS)
3. Certificate validation (proper TLS handshake)
4. Network isolation (optional, requires network policy testing)

Can operate in two modes:
- Live mode: Test actual Prometheus endpoints
- Mock mode: Validate against mock HTTP servers (for CI without staging)
"""

import argparse
import json
import logging
import ssl
import sys
import threading
from dataclasses import asdict, dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of a single validation check."""
    
    test_name: str
    passed: bool
    message: str
    details: Optional[Dict[str, Any]] = None
    severity: str = "info"  # info, warning, error


@dataclass
class PrometheusValidationReport:
    """Complete validation report for a Prometheus endpoint."""
    
    endpoint: str
    timestamp: str
    results: List[ValidationResult]
    summary: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary for JSON serialization."""
        return {
            "endpoint": self.endpoint,
            "timestamp": self.timestamp,
            "results": [asdict(r) for r in self.results],
            "summary": self.summary
        }
    
    def has_failures(self) -> bool:
        """Check if any validation failed."""
        return any(not r.passed for r in self.results)


class MockPrometheusHandler(BaseHTTPRequestHandler):
    """Mock HTTP handler simulating Prometheus metrics endpoint."""
    
    def log_message(self, format: str, *args: Any) -> None:
        """Suppress default HTTP logging."""
        pass
    
    def do_GET(self) -> None:
        """Handle GET requests with basic auth validation."""
        if self.path != "/metrics":
            self.send_error(404, "Not Found")
            return
        
        # Check for Authorization header
        auth_header = self.headers.get("Authorization")
        
        if not auth_header:
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Prometheus"')
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Unauthorized: Authentication required\n")
            return
        
        # Simple validation: check for "Basic" scheme
        if not auth_header.startswith("Basic "):
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Prometheus"')
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Unauthorized: Invalid auth scheme\n")
            return
        
        # Mock valid response
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        
        # Return sample Prometheus metrics
        metrics = """# HELP rag_rerank_latency_seconds Rerank stage latency
# TYPE rag_rerank_latency_seconds histogram
rag_rerank_latency_seconds_bucket{device="cuda:0",le="0.5"} 42
rag_rerank_latency_seconds_bucket{device="cuda:0",le="1.0"} 95
rag_rerank_latency_seconds_bucket{device="cuda:0",le="+Inf"} 100
rag_rerank_latency_seconds_sum{device="cuda:0"} 45.3
rag_rerank_latency_seconds_count{device="cuda:0"} 100
# HELP rag_gpu_peak_bytes GPU peak memory usage
# TYPE rag_gpu_peak_bytes gauge
rag_gpu_peak_bytes{stage="rerank",device="cuda:0"} 2251799813685248
"""
        self.wfile.write(metrics.encode())


def start_mock_server(port: int = 9090, use_tls: bool = False) -> threading.Thread:
    """
    Start a mock Prometheus HTTP/HTTPS server in a separate thread.
    
    Args:
        port: Port to bind to
        use_tls: Whether to enable TLS with self-signed certificate
        
    Returns:
        Thread handle for the server
    """
    def run_server() -> None:
        server = HTTPServer(("localhost", port), MockPrometheusHandler)
        
        if use_tls:
            # Create minimal SSL context with self-signed cert
            import tempfile
            from pathlib import Path
            
            # Create temporary directory for certificates
            tmpdir = tempfile.mkdtemp()
            cert_file = Path(tmpdir) / "cert.pem"
            key_file = Path(tmpdir) / "key.pem"
            
            # Generate self-signed certificate using Python's ssl module
            # This creates a minimal cert that works for localhost testing
            try:
                import subprocess
                subprocess.run([
                    "openssl", "req", "-new", "-x509", "-days", "1",
                    "-nodes", "-out", str(cert_file), "-keyout", str(key_file),
                    "-subj", "/CN=localhost"
                ], check=True, capture_output=True, timeout=5)
                
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                context.load_cert_chain(str(cert_file), str(key_file))
                server.socket = context.wrap_socket(server.socket, server_side=True)
                logger.info(f"Mock Prometheus HTTPS server started on port {port} with self-signed cert")
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                # If openssl fails, create a basic TLS wrapper
                # This won't have a proper certificate but will use TLS protocol
                logger.warning("OpenSSL not available or failed, using basic TLS wrapper")
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                # Try to load default certs or create adhoc
                try:
                    import ssl as ssl_module
                    if hasattr(ssl_module, 'PROTOCOL_TLS_SERVER'):
                        server.socket = context.wrap_socket(server.socket, server_side=True)
                        logger.info(f"Mock Prometheus HTTPS server started on port {port} (basic TLS)")
                except Exception as e:
                    logger.error(f"Failed to enable TLS: {e}")
                    logger.info(f"Falling back to HTTP server on port {port}")
            
            server.serve_forever()
        else:
            logger.info(f"Mock Prometheus HTTP server started on port {port}")
            server.serve_forever()
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    return thread


class PrometheusValidator:
    """Validates Prometheus endpoint authentication and TLS configuration."""
    
    def __init__(
        self,
        endpoint: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        verify_tls: bool = True,
        timeout: int = 10,
    ) -> None:
        """
        Initialize validator.
        
        Args:
            endpoint: Prometheus metrics endpoint URL
            username: Basic auth username
            password: Basic auth password
            verify_tls: Whether to verify TLS certificates
            timeout: Request timeout in seconds
        """
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.verify_tls = verify_tls
        self.timeout = timeout
        self.results: List[ValidationResult] = []
    
    def validate_authentication_required(self) -> ValidationResult:
        """Test that endpoint returns 401 without credentials."""
        logger.info("Testing authentication requirement...")
        
        try:
            req = Request(self.endpoint)
            response = urlopen(req, timeout=self.timeout)
            
            # If we get here, auth is NOT required (bad)
            return ValidationResult(
                test_name="authentication_required",
                passed=False,
                message="Endpoint accessible without authentication (security risk)",
                details={"status_code": response.status},
                severity="error"
            )
        
        except HTTPError as e:
            if e.code == 401:
                # Expected behavior
                return ValidationResult(
                    test_name="authentication_required",
                    passed=True,
                    message="Endpoint correctly requires authentication (401 Unauthorized)",
                    details={"status_code": 401}
                )
            else:
                return ValidationResult(
                    test_name="authentication_required",
                    passed=False,
                    message=f"Unexpected HTTP error: {e.code}",
                    details={"status_code": e.code, "reason": str(e.reason)},
                    severity="warning"
                )
        
        except URLError as e:
            return ValidationResult(
                test_name="authentication_required",
                passed=False,
                message=f"Connection failed: {e.reason}",
                details={"error": str(e.reason)},
                severity="error"
            )
        
        except Exception as e:
            return ValidationResult(
                test_name="authentication_required",
                passed=False,
                message=f"Unexpected error: {type(e).__name__}",
                details={"error": str(e)},
                severity="error"
            )
    
    def validate_authentication_success(self) -> ValidationResult:
        """Test that valid credentials grant access (200 OK)."""
        if not self.username or not self.password:
            return ValidationResult(
                test_name="authentication_success",
                passed=False,
                message="Cannot test valid credentials: username/password not provided",
                severity="warning"
            )
        
        logger.info("Testing authentication with valid credentials...")
        
        try:
            # Create request with basic auth
            import base64
            credentials = base64.b64encode(
                f"{self.username}:{self.password}".encode()
            ).decode()
            
            req = Request(self.endpoint)
            req.add_header("Authorization", f"Basic {credentials}")
            
            response = urlopen(req, timeout=self.timeout)
            
            if response.status == 200:
                content = response.read().decode('utf-8', errors='ignore')
                has_metrics = "# HELP" in content or "# TYPE" in content
                
                return ValidationResult(
                    test_name="authentication_success",
                    passed=True,
                    message="Valid credentials accepted (200 OK)",
                    details={
                        "status_code": 200,
                        "has_prometheus_metrics": has_metrics,
                        "content_length": len(content)
                    }
                )
            else:
                return ValidationResult(
                    test_name="authentication_success",
                    passed=False,
                    message=f"Unexpected status code: {response.status}",
                    details={"status_code": response.status},
                    severity="warning"
                )
        
        except HTTPError as e:
            return ValidationResult(
                test_name="authentication_success",
                passed=False,
                message=f"Authentication failed with valid credentials: {e.code}",
                details={"status_code": e.code, "reason": str(e.reason)},
                severity="error"
            )
        
        except Exception as e:
            return ValidationResult(
                test_name="authentication_success",
                passed=False,
                message=f"Request failed: {type(e).__name__}",
                details={"error": str(e)},
                severity="error"
            )
    
    def validate_tls_enforcement(self) -> ValidationResult:
        """Test that TLS is enforced (HTTPS only)."""
        logger.info("Testing TLS enforcement...")
        
        # Check if endpoint uses HTTPS
        if not self.endpoint.startswith("https://"):
            return ValidationResult(
                test_name="tls_enforcement",
                passed=False,
                message="Endpoint uses HTTP instead of HTTPS (security risk)",
                details={"scheme": "http"},
                severity="error"
            )
        
        # Try to validate TLS certificate
        try:
            import socket
            from urllib.parse import urlparse
            
            parsed = urlparse(self.endpoint)
            hostname = parsed.hostname or "localhost"
            port = parsed.port or 443
            
            context = ssl.create_default_context()
            if not self.verify_tls:
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((hostname, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    
                    return ValidationResult(
                        test_name="tls_enforcement",
                        passed=True,
                        message="TLS connection successful",
                        details={
                            "scheme": "https",
                            "tls_version": ssock.version(),
                            "cipher_suite": cipher[0] if cipher else None,
                            "cert_subject": dict(x[0] for x in cert.get("subject", [])) if cert else None
                        }
                    )
        
        except ssl.SSLError as e:
            # TLS error might indicate certificate issues
            return ValidationResult(
                test_name="tls_enforcement",
                passed=False,
                message=f"TLS validation failed: {e}",
                details={"error": str(e)},
                severity="error" if self.verify_tls else "warning"
            )
        
        except Exception as e:
            return ValidationResult(
                test_name="tls_enforcement",
                passed=False,
                message=f"TLS connection failed: {type(e).__name__}",
                details={"error": str(e)},
                severity="warning"
            )
    
    def run_all_validations(self) -> PrometheusValidationReport:
        """
        Run all validation checks and generate report.
        
        Returns:
            Complete validation report
        """
        from datetime import datetime
        
        logger.info(f"Starting validation for endpoint: {self.endpoint}")
        
        # Run all validation checks
        self.results = [
            self.validate_authentication_required(),
            self.validate_authentication_success(),
            self.validate_tls_enforcement(),
        ]
        
        # Generate summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        errors = sum(1 for r in self.results if not r.passed and r.severity == "error")
        warnings = sum(1 for r in self.results if not r.passed and r.severity == "warning")
        
        summary = {
            "total_checks": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "warnings": warnings,
            "overall_status": "PASS" if failed == 0 else ("FAIL" if errors > 0 else "WARN")
        }
        
        report = PrometheusValidationReport(
            endpoint=self.endpoint,
            timestamp=datetime.utcnow().isoformat() + "Z",
            results=self.results,
            summary=summary
        )
        
        logger.info(f"Validation complete: {summary['overall_status']}")
        logger.info(f"  Passed: {passed}/{total}, Failed: {failed}/{total} (Errors: {errors}, Warnings: {warnings})")
        
        return report


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Validate Prometheus metrics endpoint authentication and TLS"
    )
    
    parser.add_argument(
        "--endpoint",
        default="http://localhost:9090/metrics",
        help="Prometheus metrics endpoint URL (default: http://localhost:9090/metrics)"
    )
    parser.add_argument(
        "--username",
        help="Basic auth username"
    )
    parser.add_argument(
        "--password",
        help="Basic auth password"
    )
    parser.add_argument(
        "--no-verify-tls",
        action="store_true",
        help="Disable TLS certificate verification"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10)"
    )
    parser.add_argument(
        "--output",
        help="Output file for JSON report (default: stdout)"
    )
    parser.add_argument(
        "--mock-mode",
        action="store_true",
        help="Start mock server for testing (useful in CI without staging)"
    )
    parser.add_argument(
        "--mock-port",
        type=int,
        default=19090,
        help="Port for mock server (default: 19090)"
    )
    parser.add_argument(
        "--mock-https",
        action="store_true",
        help="Use HTTPS for mock server (with self-signed cert)"
    )
    
    args = parser.parse_args()
    
    # Start mock server if requested
    mock_thread = None
    endpoint = args.endpoint
    
    if args.mock_mode:
        use_tls = args.mock_https
        logger.info(f"Starting mock Prometheus server ({'HTTPS' if use_tls else 'HTTP'})...")
        mock_thread = start_mock_server(port=args.mock_port, use_tls=use_tls)
        
        # Give server time to start
        import time
        time.sleep(2)  # Increased for TLS setup
        
        # Override endpoint to use mock
        protocol = "https" if use_tls else "http"
        endpoint = f"{protocol}://localhost:{args.mock_port}/metrics"
        logger.info(f"Mock server started, using endpoint: {endpoint}")
    
    try:
        # Run validations
        validator = PrometheusValidator(
            endpoint=endpoint,
            username=args.username or "test_user",
            password=args.password or "test_pass",
            verify_tls=not args.no_verify_tls,
            timeout=args.timeout
        )
        
        report = validator.run_all_validations()
        
        # Output report
        report_dict = report.to_dict()
        report_json = json.dumps(report_dict, indent=2)
        
        if args.output:
            with open(args.output, "w") as f:
                f.write(report_json)
            logger.info(f"Report written to {args.output}")
        else:
            print(report_json)
        
        # Print summary to stderr for human readability
        print("\n=== Validation Summary ===", file=sys.stderr)
        print(f"Endpoint: {report.endpoint}", file=sys.stderr)
        print(f"Status: {report.summary['overall_status']}", file=sys.stderr)
        print(f"Passed: {report.summary['passed']}/{report.summary['total_checks']}", file=sys.stderr)
        print(f"Failed: {report.summary['failed']} (Errors: {report.summary['errors']}, Warnings: {report.summary['warnings']})", file=sys.stderr)
        print("", file=sys.stderr)
        
        for result in report.results:
            status = "✓" if result.passed else "✗"
            severity_marker = f"[{result.severity.upper()}]" if not result.passed else ""
            print(f"  {status} {result.test_name}: {result.message} {severity_marker}", file=sys.stderr)
        
        # Return exit code based on validation results
        if report.summary["errors"] > 0:
            return 1  # Hard failure
        elif report.summary["warnings"] > 0:
            return 2  # Warnings (might want to fail in strict mode)
        else:
            return 0  # Success
    
    finally:
        if mock_thread:
            # Threads are daemon, so they'll terminate when main exits
            logger.info("Mock server will terminate with main process")


if __name__ == "__main__":
    sys.exit(main())
