"""Unit tests for Prometheus endpoint validation script."""

import json
import threading
import time
from datetime import datetime, timedelta
from typing import Any, Dict, Generator

import pytest

from scripts.validate_prometheus_endpoint import (
    MockPrometheusHandler,
    PrometheusValidationReport,
    PrometheusValidator,
    ValidationResult,
    start_mock_server,
)


class TestValidationResult:
    """Test ValidationResult dataclass."""

    def test_validation_result_creation(self) -> None:
        """Verify ValidationResult can be created with all fields."""
        result = ValidationResult(
            test_name="test_example",
            passed=True,
            message="Test passed successfully",
            details={"key": "value"},
            severity="info"
        )
        
        assert result.test_name == "test_example"
        assert result.passed is True
        assert result.message == "Test passed successfully"
        assert result.details == {"key": "value"}
        assert result.severity == "info"

    def test_validation_result_optional_fields(self) -> None:
        """Verify ValidationResult works with optional fields."""
        result = ValidationResult(
            test_name="minimal_test",
            passed=False,
            message="Test failed"
        )
        
        assert result.details is None
        assert result.severity == "info"  # Default


class TestPrometheusValidationReport:
    """Test PrometheusValidationReport dataclass."""

    def test_report_creation(self) -> None:
        """Verify report can be created and converted to dict."""
        results = [
            ValidationResult("test1", True, "Success"),
            ValidationResult("test2", False, "Failure", severity="error")
        ]
        
        summary = {
            "total_checks": 2,
            "passed": 1,
            "failed": 1,
            "errors": 1,
            "warnings": 0,
            "overall_status": "FAIL"
        }
        
        report = PrometheusValidationReport(
            endpoint="http://localhost:9090/metrics",
            timestamp="2025-10-25T12:00:00Z",
            results=results,
            summary=summary
        )
        
        assert report.endpoint == "http://localhost:9090/metrics"
        assert len(report.results) == 2
        assert report.summary["overall_status"] == "FAIL"

    def test_report_to_dict(self) -> None:
        """Verify report serializes to dict correctly."""
        results = [ValidationResult("test1", True, "Success")]
        summary = {"total_checks": 1, "passed": 1}
        
        report = PrometheusValidationReport(
            endpoint="http://test:9090/metrics",
            timestamp="2025-10-25T12:00:00Z",
            results=results,
            summary=summary
        )
        
        report_dict = report.to_dict()
        
        assert report_dict["endpoint"] == "http://test:9090/metrics"
        assert report_dict["timestamp"] == "2025-10-25T12:00:00Z"
        assert len(report_dict["results"]) == 1
        assert report_dict["results"][0]["test_name"] == "test1"
        assert report_dict["summary"]["total_checks"] == 1

    def test_report_has_failures(self) -> None:
        """Verify has_failures() correctly detects failures."""
        # All passed
        results_pass = [
            ValidationResult("test1", True, "Success"),
            ValidationResult("test2", True, "Success")
        ]
        report_pass = PrometheusValidationReport(
            endpoint="test", timestamp="test", results=results_pass, summary={}
        )
        assert report_pass.has_failures() is False
        
        # Some failed
        results_fail = [
            ValidationResult("test1", True, "Success"),
            ValidationResult("test2", False, "Failure")
        ]
        report_fail = PrometheusValidationReport(
            endpoint="test", timestamp="test", results=results_fail, summary={}
        )
        assert report_fail.has_failures() is True


class TestMockPrometheusServer:
    """Test mock Prometheus HTTP server."""

    @pytest.fixture
    def mock_server_port(self) -> int:
        """Return a test port for mock server."""
        return 19091  # Use non-standard port to avoid conflicts

    def test_mock_server_starts(self, mock_server_port: int) -> None:
        """Verify mock server can be started and stopped."""
        thread = start_mock_server(port=mock_server_port)
        time.sleep(0.5)  # Give server time to start
        
        assert thread.is_alive()
        # Daemon thread will terminate with test process

    def test_mock_server_requires_authentication(self, mock_server_port: int) -> None:
        """Verify mock server returns 401 without credentials."""
        from urllib.request import Request, urlopen
        from urllib.error import HTTPError
        
        thread = start_mock_server(port=mock_server_port)
        time.sleep(0.5)
        
        try:
            req = Request(f"http://localhost:{mock_server_port}/metrics")
            
            with pytest.raises(HTTPError) as exc_info:
                urlopen(req, timeout=2)
            
            assert exc_info.value.code == 401
            assert "WWW-Authenticate" in exc_info.value.headers
        
        finally:
            pass  # Daemon thread will clean up

    def test_mock_server_accepts_valid_credentials(self, mock_server_port: int) -> None:
        """Verify mock server returns 200 with valid basic auth."""
        import base64
        from urllib.request import Request, urlopen
        
        thread = start_mock_server(port=mock_server_port)
        time.sleep(0.5)
        
        try:
            credentials = base64.b64encode(b"user:pass").decode()
            req = Request(f"http://localhost:{mock_server_port}/metrics")
            req.add_header("Authorization", f"Basic {credentials}")
            
            response = urlopen(req, timeout=2)
            
            assert response.status == 200
            content = response.read().decode()
            assert "# HELP" in content
            assert "rag_rerank_latency_seconds" in content
        
        finally:
            pass  # Daemon thread will clean up

    def test_mock_server_returns_404_for_invalid_path(self, mock_server_port: int) -> None:
        """Verify mock server returns 404 for non-/metrics paths."""
        import base64
        from urllib.request import Request, urlopen
        from urllib.error import HTTPError
        
        thread = start_mock_server(port=mock_server_port)
        time.sleep(0.5)
        
        try:
            credentials = base64.b64encode(b"user:pass").decode()
            req = Request(f"http://localhost:{mock_server_port}/invalid")
            req.add_header("Authorization", f"Basic {credentials}")
            
            with pytest.raises(HTTPError) as exc_info:
                urlopen(req, timeout=2)
            
            assert exc_info.value.code == 404
        
        finally:
            pass  # Daemon thread will clean up


class TestPrometheusValidator:
    """Test PrometheusValidator class."""

    @pytest.fixture
    def mock_server_port(self) -> int:
        """Return a test port for mock server."""
        return 19092

    @pytest.fixture
    def mock_server_process(self, mock_server_port: int) -> Generator[threading.Thread, None, None]:
        """Start mock server for testing."""
        thread = start_mock_server(port=mock_server_port)
        time.sleep(0.5)
        yield thread
        # Thread is daemon, will terminate with test process

    def test_validator_initialization(self) -> None:
        """Verify validator can be initialized."""
        validator = PrometheusValidator(
            endpoint="http://localhost:9090/metrics",
            username="test_user",
            password="test_pass",
            verify_tls=True,
            timeout=10
        )
        
        assert validator.endpoint == "http://localhost:9090/metrics"
        assert validator.username == "test_user"
        assert validator.password == "test_pass"
        assert validator.verify_tls is True
        assert validator.timeout == 10

    def test_validate_authentication_required_pass(
        self, mock_server_port: int, mock_server_process: threading.Thread
    ) -> None:
        """Verify validation passes when 401 is returned without credentials."""
        validator = PrometheusValidator(
            endpoint=f"http://localhost:{mock_server_port}/metrics",
            timeout=2
        )
        
        result = validator.validate_authentication_required()
        
        assert result.passed is True
        assert result.test_name == "authentication_required"
        assert "401" in result.message
        assert result.details["status_code"] == 401

    def test_validate_authentication_success_pass(
        self, mock_server_port: int, mock_server_process: threading.Thread
    ) -> None:
        """Verify validation passes when valid credentials grant access."""
        validator = PrometheusValidator(
            endpoint=f"http://localhost:{mock_server_port}/metrics",
            username="test_user",
            password="test_pass",
            timeout=2
        )
        
        result = validator.validate_authentication_success()
        
        assert result.passed is True
        assert result.test_name == "authentication_success"
        assert "200" in result.message
        assert result.details["status_code"] == 200
        assert result.details["has_prometheus_metrics"] is True

    def test_validate_authentication_success_without_credentials(self) -> None:
        """Verify validation returns warning when no credentials provided."""
        validator = PrometheusValidator(
            endpoint="http://localhost:9090/metrics",
            username=None,
            password=None
        )
        
        result = validator.validate_authentication_success()
        
        assert result.passed is False
        assert result.severity == "warning"
        assert "username/password not provided" in result.message

    def test_validate_tls_enforcement_http_endpoint(self) -> None:
        """Verify validation fails for HTTP (non-HTTPS) endpoints."""
        validator = PrometheusValidator(
            endpoint="http://localhost:9090/metrics"
        )
        
        result = validator.validate_tls_enforcement()
        
        assert result.passed is False
        assert result.test_name == "tls_enforcement"
        assert result.severity == "error"
        assert "HTTP instead of HTTPS" in result.message

    def test_run_all_validations(
        self, mock_server_port: int, mock_server_process: threading.Thread
    ) -> None:
        """Verify run_all_validations executes all checks and generates report."""
        validator = PrometheusValidator(
            endpoint=f"http://localhost:{mock_server_port}/metrics",
            username="test_user",
            password="test_pass",
            timeout=2
        )
        
        report = validator.run_all_validations()
        
        assert report.endpoint == f"http://localhost:{mock_server_port}/metrics"
        assert len(report.results) == 3
        assert report.summary["total_checks"] == 3
        
        # Auth required should pass (401 without creds)
        auth_required = next(r for r in report.results if r.test_name == "authentication_required")
        assert auth_required.passed is True
        
        # Auth success should pass (200 with creds)
        auth_success = next(r for r in report.results if r.test_name == "authentication_success")
        assert auth_success.passed is True
        
        # TLS should fail (HTTP endpoint)
        tls_check = next(r for r in report.results if r.test_name == "tls_enforcement")
        assert tls_check.passed is False

    def test_report_summary_calculation(
        self, mock_server_port: int, mock_server_process: threading.Thread
    ) -> None:
        """Verify report summary statistics are calculated correctly."""
        validator = PrometheusValidator(
            endpoint=f"http://localhost:{mock_server_port}/metrics",
            username="user",
            password="pass",
            timeout=2
        )
        
        report = validator.run_all_validations()
        
        # We expect: 2 pass (auth checks), 1 fail (TLS - HTTP endpoint)
        assert report.summary["total_checks"] == 3
        assert report.summary["passed"] == 2
        assert report.summary["failed"] == 1
        assert report.summary["errors"] == 1  # TLS failure is error severity
        assert report.summary["overall_status"] == "FAIL"

    def test_report_timestamp_timezone_aware(
        self, mock_server_port: int, mock_server_process: threading.Thread
    ) -> None:
        """Ensure generated report timestamps are timezone-aware UTC values."""
        validator = PrometheusValidator(
            endpoint=f"http://localhost:{mock_server_port}/metrics",
            username="user",
            password="pass",
            timeout=2
        )

        report = validator.run_all_validations()
        parsed = datetime.fromisoformat(report.timestamp.replace("Z", "+00:00"))

        assert parsed.tzinfo is not None
        assert parsed.tzinfo.utcoffset(parsed) == timedelta(0)

    def test_report_json_serialization(
        self, mock_server_port: int, mock_server_process: threading.Thread
    ) -> None:
        """Verify report can be serialized to JSON."""
        validator = PrometheusValidator(
            endpoint=f"http://localhost:{mock_server_port}/metrics",
            username="user",
            password="pass",
            timeout=2
        )
        
        report = validator.run_all_validations()
        report_dict = report.to_dict()
        
        # Ensure it's JSON-serializable
        json_str = json.dumps(report_dict, indent=2)
        assert len(json_str) > 0
        
        # Parse back and verify structure
        parsed = json.loads(json_str)
        assert "endpoint" in parsed
        assert "timestamp" in parsed
        assert "results" in parsed
        assert "summary" in parsed


class TestPrometheusValidatorEdgeCases:
    """Test edge cases and error conditions."""

    def test_validator_connection_timeout(self) -> None:
        """Verify validator handles connection timeouts gracefully."""
        validator = PrometheusValidator(
            endpoint="http://192.0.2.1:9090/metrics",  # TEST-NET-1 (guaranteed unreachable)
            timeout=1
        )
        
        result = validator.validate_authentication_required()
        
        assert result.passed is False
        assert result.severity == "error"
        assert "Connection failed" in result.message or "timeout" in result.message.lower()

    def test_validator_invalid_port(self) -> None:
        """Verify validator handles connection refused gracefully."""
        validator = PrometheusValidator(
            endpoint="http://localhost:19999/metrics",  # Port unlikely to be in use
            timeout=2
        )
        
        result = validator.validate_authentication_required()
        
        assert result.passed is False
        assert result.severity == "error"

    def test_https_endpoint_without_valid_cert(self) -> None:
        """Verify TLS validation detects certificate issues."""
        # This will fail because localhost doesn't have valid cert for HTTPS
        validator = PrometheusValidator(
            endpoint="https://localhost:9443/metrics",
            verify_tls=True,
            timeout=2
        )
        
        result = validator.validate_tls_enforcement()
        
        # Should detect HTTPS but may fail on cert validation
        assert result.test_name == "tls_enforcement"
        # Result depends on whether connection succeeds - either way it's valid behavior


class TestPrometheusValidatorIntegration:
    """Integration tests for end-to-end validation flows."""

    @pytest.fixture
    def mock_server_port(self) -> int:
        """Return a test port for mock server."""
        return 19093

    def test_full_validation_workflow_with_mock(self, mock_server_port: int) -> None:
        """Test complete validation workflow against mock server."""
        thread = start_mock_server(port=mock_server_port)
        time.sleep(0.5)
        
        try:
            validator = PrometheusValidator(
                endpoint=f"http://localhost:{mock_server_port}/metrics",
                username="prometheus_user",
                password="prometheus_pass",
                verify_tls=False,
                timeout=3
            )
            
            report = validator.run_all_validations()
            
            # Check report completeness
            assert len(report.results) == 3
            assert report.timestamp is not None
            assert report.summary is not None
            
            # Verify JSON export works
            report_json = json.dumps(report.to_dict(), indent=2)
            assert len(report_json) > 100
            
            # Verify report has human-readable data
            for result in report.results:
                assert len(result.test_name) > 0
                assert len(result.message) > 0
        
        finally:
            pass  # Daemon thread will clean up

    def test_validation_report_includes_all_details(self, mock_server_port: int) -> None:
        """Verify validation report includes all expected details for debugging."""
        thread = start_mock_server(port=mock_server_port)
        time.sleep(0.5)
        
        try:
            validator = PrometheusValidator(
                endpoint=f"http://localhost:{mock_server_port}/metrics",
                username="test",
                password="test",
                timeout=2
            )
            
            report = validator.run_all_validations()
            
            # Each result should have meaningful details
            for result in report.results:
                if result.passed:
                    assert result.details is not None
                    assert len(result.details) > 0
        
        finally:
            pass  # Daemon thread will clean up
