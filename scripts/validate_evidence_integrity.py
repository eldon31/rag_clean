#!/usr/bin/env python3
"""
Evidence Integrity Validator

Compares CLI log files with processing summary JSON files to detect contradictions
between claimed behavior and actual execution. Created to prevent QA gate issues
where evidence artifacts contain contradictory metadata.

Exit Codes:
    0: All checks pass
    1: Contradictions found
    2: Validation errors (files missing, parse errors)

Usage:
    python validate_evidence_integrity.py <cli_log_path> <processing_summary_json_path>
    
Story Reference: Story 1.4 (EVI-201, DOC-221)
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from processor.ultimate_embedder.summary import normalize_processing_summary


@dataclass
class CLILogData:
    """Parsed data from CLI execution log."""

    device_mode: Optional[str] = None
    sparse_model_status: Optional[str] = None
    sparse_model_name: Optional[str] = None
    sparse_failure_reason: Optional[str] = None
    enable_rerank: Optional[bool] = None
    enable_sparse: Optional[bool] = None
    cuda_devices_detected: List[str] = field(default_factory=list)


@dataclass
class ProcessingSummaryData:
    """Parsed data from processing summary JSON."""

    device_info: Optional[str] = None
    sparse_model_status: Optional[str] = None
    sparse_model_name: Optional[str] = None
    cuda_used: Optional[bool] = None
    stage_statuses: Dict[str, str] = field(default_factory=dict)


@dataclass
class Contradiction:
    """Detected contradiction between CLI log and processing summary."""

    severity: str  # critical, high, medium
    category: str  # device, sparse, metadata
    message: str


def parse_cli_log(log_path: Path) -> CLILogData:
    """Parse CLI log file to extract device mode, sparse model status, and toggles."""

    data = CLILogData()

    try:
        # Try different encodings
        encodings = ["utf-8", "utf-16", "latin-1", "cp1252"]
        content = None

        for encoding in encodings:
            try:
                with open(log_path, "r", encoding=encoding) as f:
                    content = f.read()
                break
            except (UnicodeDecodeError, UnicodeError):
                continue

        if content is None:
            print(f"Error: Unable to decode {log_path} with any known encoding", file=sys.stderr)
            sys.exit(2)

        for line in content.splitlines():
                # Device detection
                if "No GPU detected; falling back to CPU mode" in line:
                    data.device_mode = "CPU"
                elif re.search(r"CUDA available.*devices?: (\d+)", line, re.IGNORECASE):
                    match = re.search(r"devices?: (\d+)", line)
                    if match:
                        data.device_mode = "GPU"
                        data.cuda_devices_detected.append(match.group(1))

                # Sparse model status
                if "Failed to load sparse model" in line:
                    data.sparse_model_status = "failed"
                    # Extract model name
                    match = re.search(r"Failed to load sparse model (\S+):", line)
                    if match:
                        data.sparse_model_name = match.group(1)
                    # Extract failure reason
                    match = re.search(r"Failed to load sparse model.*?: (.+)$", line)
                    if match:
                        data.sparse_failure_reason = match.group(1).strip()

                elif re.search(r"Sparse model (\S+) (loaded|staged)", line):
                    data.sparse_model_status = "loaded"
                    match = re.search(r"Sparse model (\S+)", line)
                    if match:
                        data.sparse_model_name = match.group(1)

                # Feature toggles
                if "enable_rerank  => True" in line or "enable_rerank=True" in line:
                    data.enable_rerank = True
                elif "enable_rerank  => False" in line or "enable_rerank=False" in line:
                    data.enable_rerank = False

                if "enable_sparse  => True" in line or "enable_sparse=True" in line:
                    data.enable_sparse = True
                elif "enable_sparse  => False" in line or "enable_sparse=False" in line:
                    data.enable_sparse = False

    except Exception as e:
        print(f"Error parsing CLI log {log_path}: {e}", file=sys.stderr)
        sys.exit(2)

    return data


def parse_processing_summary(json_path: Path) -> ProcessingSummaryData:
    """Parse processing summary JSON to extract device info and sparse model status."""

    data = ProcessingSummaryData()

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        content = normalize_processing_summary(content)

        # Check dense_run for GPU lease events
        dense_run = content.get("dense_run", {})
        lease_events = dense_run.get("lease_events", [])
        if lease_events:
            # Check if any CUDA devices were leased
            cuda_devices = [e.get("device_ids", []) for e in lease_events if "cuda" in str(e.get("device_ids", []))]
            if cuda_devices:
                data.cuda_used = True
                data.device_info = f"cuda (leased devices: {cuda_devices[0]})"

        # Check rerank_run for device info
        rerank_run = content.get("rerank_run", {})
        if rerank_run.get("device") and "cuda" in rerank_run.get("device", ""):
            data.cuda_used = True
            if not data.device_info:
                data.device_info = rerank_run.get("device")

        # Check sparse_run for device and model info
        sparse_run = content.get("sparse_run", {})
        if sparse_run:
            data.sparse_model_status = "loaded" if sparse_run.get("executed") else "not_executed"
            models = sparse_run.get("models", [])
            if models:
                data.sparse_model_name = models[0] if isinstance(models, list) else models

            # Check sparse devices
            sparse_devices = sparse_run.get("devices", {})
            if sparse_devices and any("cuda" in str(v) for v in sparse_devices.values()):
                data.cuda_used = True
                if not data.device_info:
                    data.device_info = f"cuda (sparse: {list(sparse_devices.values())})"

        # Extract device information from metadata (fallback)
        metadata = content.get("metadata", {})
        if not data.device_info:
            data.device_info = metadata.get("device") or metadata.get("device_type")

        # Check CUDA usage from metadata (fallback)
        if data.cuda_used is None:
            if "cuda" in metadata:
                data.cuda_used = metadata["cuda"]
            elif data.device_info:
                data.cuda_used = "cuda" in data.device_info.lower()

        # Extract sparse model status from telemetry (fallback)
        if not data.sparse_model_status:
            telemetry = content.get("telemetry", {})
            sparse_telemetry = telemetry.get("sparse", {})
            if sparse_telemetry:
                data.sparse_model_status = sparse_telemetry.get("status")

    except Exception as e:
        print(f"Error parsing processing summary {json_path}: {e}", file=sys.stderr)
        sys.exit(2)

    return data


def compare_evidence(cli: CLILogData, summary: ProcessingSummaryData) -> List[Contradiction]:
    """Compare CLI log and processing summary for contradictions."""

    contradictions: List[Contradiction] = []

    # Device mode contradictions (CRITICAL)
    if cli.device_mode == "CPU" and summary.cuda_used:
        contradictions.append(
            Contradiction(
                severity="critical",
                category="device",
                message=f"CLI log shows CPU fallback (device_mode={cli.device_mode}), "
                f"but processing summary claims CUDA usage (cuda={summary.cuda_used})",
            )
        )

    if cli.device_mode == "GPU" and summary.device_info and "cpu" in summary.device_info.lower():
        contradictions.append(
            Contradiction(
                severity="critical",
                category="device",
                message=f"CLI log shows GPU execution (device_mode={cli.device_mode}), "
                f"but processing summary claims CPU (device={summary.device_info})",
            )
        )

    # Sparse model contradictions (HIGH)
    if cli.sparse_model_status == "failed" and summary.sparse_model_status in ["loaded", "success"]:
        contradictions.append(
            Contradiction(
                severity="high",
                category="sparse",
                message=f"CLI log shows sparse model load failure (model={cli.sparse_model_name}, "
                f"reason={cli.sparse_failure_reason}), but processing summary claims success "
                f"(status={summary.sparse_model_status}, model={summary.sparse_model_name})",
            )
        )

    if cli.sparse_model_status == "loaded" and summary.sparse_model_status in ["failed", "error"]:
        contradictions.append(
            Contradiction(
                severity="high",
                category="sparse",
                message=f"CLI log shows sparse model loaded (model={cli.sparse_model_name}), "
                f"but processing summary claims failure (status={summary.sparse_model_status})",
            )
        )

    # Sparse model name mismatch (MEDIUM)
    if (
        cli.sparse_model_name
        and summary.sparse_model_name
        and cli.sparse_model_name != summary.sparse_model_name
    ):
        contradictions.append(
            Contradiction(
                severity="medium",
                category="metadata",
                message=f"Sparse model name mismatch: CLI={cli.sparse_model_name}, "
                f"summary={summary.sparse_model_name}",
            )
        )

    # Feature toggle vs execution mismatch (MEDIUM)
    if cli.enable_sparse is False and summary.sparse_model_status == "loaded":
        contradictions.append(
            Contradiction(
                severity="medium",
                category="metadata",
                message=f"CLI shows sparse disabled (enable_sparse={cli.enable_sparse}), "
                f"but summary shows sparse model loaded (status={summary.sparse_model_status})",
            )
        )

    return contradictions


def run_validation(
    cli_path: Path, summary_path: Path, verbose: bool
) -> Tuple[List[Contradiction], CLILogData, ProcessingSummaryData]:
    """Execute a single evidence validation run and return comparison details."""

    if not cli_path.is_file():
        print(f"Error: CLI log file not found: {cli_path}", file=sys.stderr)
        sys.exit(2)

    if not summary_path.is_file():
        print(
            f"Error: Processing summary file not found: {summary_path}",
            file=sys.stderr,
        )
        sys.exit(2)

    cli_data = parse_cli_log(cli_path)
    summary_data = parse_processing_summary(summary_path)

    if verbose:
        print("CLI Log Data:")
        print(f"  Device Mode: {cli_data.device_mode}")
        print(f"  Sparse Model Status: {cli_data.sparse_model_status}")
        print(f"  Sparse Model Name: {cli_data.sparse_model_name}")
        print(f"  Enable Rerank: {cli_data.enable_rerank}")
        print(f"  Enable Sparse: {cli_data.enable_sparse}")
        print()
        print("Processing Summary Data:")
        print(f"  Device Info: {summary_data.device_info}")
        print(f"  CUDA Used: {summary_data.cuda_used}")
        print(f"  Sparse Model Status: {summary_data.sparse_model_status}")
        print(f"  Sparse Model Name: {summary_data.sparse_model_name}")
        print()

    contradictions = compare_evidence(cli_data, summary_data)
    return contradictions, cli_data, summary_data


def validate_bundle(bundle_path: Path, verbose: bool) -> int:
    """Validate all CLI/summary pairs within a regression harness bundle."""

    if not bundle_path.is_dir():
        print(f"Error: Bundle path is not a directory: {bundle_path}", file=sys.stderr)
        return 2

    scenario_dirs = sorted(p for p in bundle_path.iterdir() if p.is_dir())
    if not scenario_dirs:
        print(
            f"Error: No scenario subdirectories found under bundle: {bundle_path}",
            file=sys.stderr,
        )
        return 2

    bundle_pass = True
    total_contradictions = 0

    for scenario_dir in scenario_dirs:
        cli_candidates = sorted(scenario_dir.glob("cli_*.txt"))
        summary_candidates = sorted(scenario_dir.glob("processing_summary_*.json"))

        if not cli_candidates:
            print(
                f"Error: Missing CLI log in scenario '{scenario_dir.name}'",
                file=sys.stderr,
            )
            return 2

        if not summary_candidates:
            print(
                f"Error: Missing processing summary in scenario '{scenario_dir.name}'",
                file=sys.stderr,
            )
            return 2

        cli_path = cli_candidates[0]
        summary_path = summary_candidates[0]

        print(f"Validating scenario: {scenario_dir.name}")
        contradictions, cli_data, summary_data = run_validation(
            cli_path, summary_path, verbose
        )

        if contradictions:
            bundle_pass = False
            total_contradictions += len(contradictions)
            print(
                f"Evidence Integrity Check FAILED: {len(contradictions)} contradiction(s) found"
            )
            for i, c in enumerate(contradictions, 1):
                print(f"{i}. [{c.severity.upper()}] {c.category.upper()}")
                print(f"   {c.message}")
            print()
        else:
            print("Evidence Integrity Check PASSED: No contradictions detected")
            if verbose:
                print("Verified:")
                print(
                    f"  - Device consistency: {cli_data.device_mode} ↔ {summary_data.device_info}"
                )
                print(
                    "  - Sparse model consistency: "
                    f"{cli_data.sparse_model_status} ↔ {summary_data.sparse_model_status}"
                )
                print()

    if bundle_pass:
        scenario_count = len(scenario_dirs)
        print(
            f"Bundle integrity check PASSED for {scenario_count} scenario(s)."
        )
        return 0

    print(
        "Bundle integrity check FAILED: "
        f"{total_contradictions} contradiction(s) detected across scenarios."
    )
    return 1


def main():
    parser = argparse.ArgumentParser(
        description="Validate evidence integrity between CLI logs and processing summaries"
    )
    parser.add_argument(
        "cli_log",
        type=Path,
        nargs="?",
        help="Path to CLI execution log file (omit when using --bundle)",
    )
    parser.add_argument(
        "processing_summary",
        type=Path,
        nargs="?",
        help="Path to processing summary JSON file (omit when using --bundle)",
    )
    parser.add_argument("--bundle", type=Path, help="Directory containing scenario folders")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.bundle and (args.cli_log or args.processing_summary):
        parser.error("--bundle cannot be combined with positional arguments")

    if args.bundle:
        return validate_bundle(args.bundle, args.verbose)

    if not args.cli_log or not args.processing_summary:
        parser.error("CLI log and processing summary paths are required when not using --bundle")

    contradictions, cli_data, summary_data = run_validation(
        args.cli_log, args.processing_summary, args.verbose
    )

    if contradictions:
        print(f"Evidence Integrity Check FAILED: {len(contradictions)} contradiction(s) found")
        print()

        for i, c in enumerate(contradictions, 1):
            print(f"{i}. [{c.severity.upper()}] {c.category.upper()}")
            print(f"   {c.message}")
            print()

        return 1

    print("Evidence Integrity Check PASSED: No contradictions detected")
    if args.verbose:
        print()
        print("Verified:")
        print(f"  - Device consistency: {cli_data.device_mode} ↔ {summary_data.device_info}")
        print(
            f"  - Sparse model consistency: {cli_data.sparse_model_status} ↔ {summary_data.sparse_model_status}"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
