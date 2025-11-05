#!/usr/bin/env python3
"""Run the Kaggle embed pipeline with an explicit stage status report."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Iterable, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import scripts.embed_collections_v7 as embed_v7


LOGGER = logging.getLogger("embed_stage_report")


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = embed_v7._build_parser()
    args = parser.parse_args(argv)
    # Force stage reporting for this convenience wrapper regardless of CLI overrides.
    setattr(args, "disable_stage_report", False)

    # Always keep stage messages visible, but respect quiet for other loggers.
    embed_v7._configure_logging(args.quiet)

    try:
        chunk_path, output_path = embed_v7._resolve_paths(args.chunked_dir, args.output_dir)
    except FileNotFoundError:
        return 1

    toggles = embed_v7._build_feature_toggles(args)
    LOGGER.info(
        "Feature toggles resolved: rerank=%s sparse=%s models=%s",
        toggles.enable_rerank,
        toggles.enable_sparse,
        toggles.sparse_models if toggles.sparse_models else "none",
    )
    print("[embed_stage] Feature toggles resolved. Loading chunks...", flush=True)

    embedder = embed_v7._build_embedder(args, output_path, toggles)

    primary_model = getattr(embedder, "model_name", "unknown")
    ensemble_roster = []
    if getattr(embedder, "ensemble_config", None):
        ensemble_roster = list(getattr(embedder.ensemble_config, "ensemble_models", []))

    device_label = getattr(embedder, "device", "unknown")
    device_count = getattr(embedder, "device_count", 0)

    print(f"[embed_stage] Primary model: {primary_model}", flush=True)
    if ensemble_roster:
        print("[embed_stage] Ensemble roster: " + ", ".join(ensemble_roster), flush=True)
    print(f"[embed_stage] Device: {device_label} (GPUs: {device_count})", flush=True)

    LOGGER.info("Loading chunks from %s", chunk_path)
    print(f"[embed_stage] Loading chunks from {chunk_path}...", flush=True)
    load_summary = embedder.load_chunks_from_processing(chunks_dir=str(chunk_path))
    if load_summary.get("error"):
        LOGGER.error("Chunk loading failed: %s", load_summary.get("error"))
        return 1

    total_chunks = load_summary.get("total_chunks_loaded", 0)
    if not total_chunks:
        LOGGER.error("Chunk loading produced zero chunks; verify input dataset under %s", chunk_path)
        return 1

    print(
        f"[embed_stage] Loaded {total_chunks} chunks across {load_summary.get('collections_loaded', 0)} collections.",
        flush=True,
    )

    print("[embed_stage] Starting dense ensemble...", flush=True)
    dense_results = embedder.generate_embeddings_kaggle_optimized(
        enable_monitoring=args.monitor,
        save_intermediate=args.save_intermediate,
    )
    print("[embed_stage] Dense stage complete.", flush=True)

    if isinstance(dense_results, dict):
        dense_throughput = dense_results.get("chunks_per_second")
        dense_duration = dense_results.get("processing_time_seconds")
        dense_embeddings = dense_results.get("total_embeddings_generated")
        metrics_parts = []
        if isinstance(dense_throughput, (int, float)):
            metrics_parts.append(f"throughput={dense_throughput:.2f} chunks/sec")
        if isinstance(dense_duration, (int, float)):
            metrics_parts.append(f"duration={dense_duration:.2f}s")
        if isinstance(dense_embeddings, (int, float)):
            metrics_parts.append(f"embeddings={int(dense_embeddings)}")
        if metrics_parts:
            print("[embed_stage] Dense metrics: " + ", ".join(metrics_parts), flush=True)

    inferred_prefix = args.export_prefix or embedder.get_target_collection_name()
    embedder.export_config.output_prefix = inferred_prefix

    print("[embed_stage] Exporting artefacts...", flush=True)
    exported_files = embedder.export_for_local_qdrant()
    print(f"[embed_stage] Export complete with {len(exported_files)} files.", flush=True)

    skipped_exports = dict(getattr(embedder.export_runtime, "skipped_exports", {}) or {})
    for key, reason in skipped_exports.items():
        LOGGER.warning("Export skipped for %s: %s", key, reason)
        print(f"[embed_stage] Export skipped ({key}): {reason}", flush=True)

    summary_path = (
        Path(args.summary_path)
        if args.summary_path
        else output_path / f"{inferred_prefix}_processing_summary.json"
    )
    summary = embedder.write_processing_summary(
        summary_path,
        collection_name=inferred_prefix,
        chunk_count=load_summary.get("total_chunks_loaded"),
    )
    print(f"[embed_stage] Processing summary saved to {summary_path}", flush=True)

    embed_v7._print_stage_report(embedder, summary, tag="stage")

    manifest_path = embed_v7._write_manifest(
        output_dir=output_path,
        payload={
            "collection": inferred_prefix,
            "chunks": load_summary,
            "exported_files": exported_files,
            "summary_path": str(summary_path),
        },
    )
    print(f"[embed_stage] Run manifest saved to {manifest_path}", flush=True)

    copied_log = embed_v7._copy_kaggle_log(output_path, inferred_prefix)
    if copied_log:
        print(f"[embed_stage] Copied Kaggle log to {copied_log}", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())