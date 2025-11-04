#!/usr/bin/env python3
"""Kaggle-friendly ensemble runner with rerank and sparse defaults.

This CLI is the one-command entry point for Kaggle notebooks. It mirrors the
behaviour of ``embed_collections_v6.py`` but trims the control surface so users
can simply run ``!python -m scripts.embed_collections_v7`` and immediately get:

* the exclusive three-model dense ensemble (Jina code, BGE M3, Qwen 0.6B);
* CrossEncoder reranking enabled;
* SPLADE sparse vectors exported alongside dense outputs; and
* a manifest + processing summary ready for download.

Flags remain available for advanced overrides (e.g. disable rerank) but the
ensemble + hybrid defaults require no additional arguments.
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
from pathlib import Path
from typing import Iterable, List, Optional, Sequence


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from processor.ultimate_embedder import (
    EnsembleConfig,
    FeatureToggleConfig,
    KaggleExportConfig,
    KaggleGPUConfig,
    RerankingConfig,
    UltimateKaggleEmbedderV4,
)

# ---------------------------------------------------------------------------
# Globals and defaults
# ---------------------------------------------------------------------------
LOGGER = logging.getLogger("embed_v7")
DEFAULT_ENSEMBLE = [
    "jina-code-embeddings-1.5b",
    "bge-m3",
    "qwen3-embedding-0.6b",
]
DEFAULT_SPARSE = ["splade"]
DEFAULT_RERANK_MODEL = "jina-reranker-v3"


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------
def _in_kaggle() -> bool:
    return "/kaggle" in str(Path.cwd())


def _default_chunk_dir() -> str:
    return "/kaggle/working/Chunked" if _in_kaggle() else "./Chunked"


def _default_output_dir() -> str:
    return "/kaggle/working/Embeddings" if _in_kaggle() else "./Embeddings"


def _configure_logging(quiet: bool) -> None:
    level = logging.WARNING if quiet else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")


def _resolve_paths(chunked_dir: str, output_dir: str) -> tuple[Path, Path]:
    chunk_candidate = Path(chunked_dir).expanduser()
    if not chunk_candidate.is_absolute():
        chunk_candidate = Path.cwd() / chunk_candidate
    chunk_path = chunk_candidate.resolve(strict=False)

    output_path = Path(output_dir).expanduser().resolve(strict=False)
    output_path.mkdir(parents=True, exist_ok=True)

    if not chunk_path.exists():
        if _in_kaggle():
            LOGGER.info(
                "Chunk directory %s not found; deferring to Kaggle chunk auto-discovery",
                chunk_path,
            )
        else:
            LOGGER.warning(
                "Chunk directory %s not found; loader will attempt fallback locations",
                chunk_path,
            )

    return chunk_path, output_path


def _dedupe_preserve_order(values: Sequence[str]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for item in values:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def _resolve_ensemble_models(cli_models: Optional[Sequence[str]]) -> List[str]:
    if cli_models:
        models = _dedupe_preserve_order([model.strip() for model in cli_models if model.strip()])
        if models:
            return models
        LOGGER.warning("Ignoring empty --ensemble-models override; using defaults")
    return list(DEFAULT_ENSEMBLE)


def _build_feature_toggles(args: argparse.Namespace) -> FeatureToggleConfig:
    enable_rerank = not args.disable_rerank
    enable_sparse = not args.disable_sparse
    sparse_models = _dedupe_preserve_order(args.sparse_models or DEFAULT_SPARSE)
    if not enable_sparse:
        sparse_models = []
    sources = {
        "enable_rerank": "cli:" + ("default-on" if enable_rerank else "--disable-rerank"),
        "enable_sparse": "cli:" + ("default-on" if enable_sparse else "--disable-sparse"),
        "sparse_models": "cli:" + ("override" if args.sparse_models else "default"),
    }
    resolution_events = (
        {"key": "enable_rerank", "value": enable_rerank, "source": sources["enable_rerank"], "layer": "cli"},
        {"key": "enable_sparse", "value": enable_sparse, "source": sources["enable_sparse"], "layer": "cli"},
        {"key": "sparse_models", "value": list(sparse_models), "source": sources["sparse_models"], "layer": "cli"},
    )
    return FeatureToggleConfig(
        enable_rerank=enable_rerank,
        enable_sparse=enable_sparse,
        sparse_models=list(sparse_models),
        sources=sources,
        resolution_events=resolution_events,
    )


def _build_embedder(args: argparse.Namespace, output_dir: Path, toggles: FeatureToggleConfig) -> UltimateKaggleEmbedderV4:
    ensemble_models = _resolve_ensemble_models(args.ensemble_models)
    export_prefix = args.export_prefix or "ultimate_embeddings_v7"

    ensemble_config = EnsembleConfig(
        ensemble_models=ensemble_models,
        exclusive_mode=not args.disable_exclusive,
    )
    gpu_config = KaggleGPUConfig(
        backend=args.backend,
        kaggle_environment=_in_kaggle(),
        output_path=str(output_dir),
    )
    export_config = KaggleExportConfig(
        working_dir=str(output_dir),
        output_prefix=export_prefix,
        export_sparse_jsonl=toggles.enable_sparse,
    )
    rerank_config = RerankingConfig(
        model_name=args.rerank_model,
        enable_reranking=toggles.enable_rerank,
        top_k_candidates=args.rerank_candidates,
        rerank_top_k=args.rerank_top_k,
    )

    embedder = UltimateKaggleEmbedderV4(
        model_name=ensemble_models[0],
        enable_ensemble=True,
        ensemble_config=ensemble_config,
        gpu_config=gpu_config,
        export_config=export_config,
        reranking_config=rerank_config,
        enable_sparse=toggles.enable_sparse,
        sparse_models=list(toggles.sparse_models),
        feature_toggles=toggles,
        local_files_only=args.local_files_only,
        force_cpu=args.force_cpu,
        hf_cache_dir=args.hf_cache_dir,
        refresh_cache=args.refresh_cache,
    )
    return embedder


def _write_manifest(output_dir: Path, payload: dict, filename: str = "run_manifest.json") -> Path:
    target = output_dir / filename
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return target


def _copy_kaggle_log(output_dir: Path, export_prefix: str) -> Optional[Path]:
    log_source = Path("/kaggle/working/embedding_process.log")
    if not log_source.exists():
        return None
    target = output_dir / f"{export_prefix}_embedding_process.log"
    try:
        shutil.copy2(log_source, target)
    except OSError:
        return None
    return target


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Embed a chunked knowledge base using the Kaggle ensemble defaults.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--chunked-dir", default=_default_chunk_dir(), help="Directory containing *_chunks.json files (recursively scanned).")
    parser.add_argument("--output-dir", default=_default_output_dir(), help="Directory to write embeddings, metadata, and summaries.")
    parser.add_argument("--ensemble-models", nargs="+", default=None, help="Override the ensemble roster (default keeps Kaggle trio).")
    parser.add_argument("--backend", choices=("pytorch", "onnx"), default="pytorch", help="Embedding backend selection passed to KaggleGPUConfig.")
    parser.add_argument("--export-prefix", default=None, help="Optional override for export prefix (defaults to inferred collection name).")
    parser.add_argument("--summary-path", default=None, help="Explicit processing summary output path.")
    parser.add_argument("--rerank-model", default=DEFAULT_RERANK_MODEL, help="CrossEncoder reranker model identifier.")
    parser.add_argument("--rerank-candidates", type=int, default=100, help="Candidate pool size fed into the reranker.")
    parser.add_argument("--rerank-top-k", type=int, default=20, help="Number of reranked results to keep.")
    parser.add_argument("--sparse-models", nargs="+", default=None, help="Override sparse models list (defaults to SPLADE).")
    parser.add_argument("--disable-rerank", action="store_true", help="Disable CrossEncoder reranking stage.")
    parser.add_argument("--disable-sparse", action="store_true", help="Disable sparse vector generation and export.")
    parser.add_argument("--disable-exclusive", action="store_true", help="Run ensemble without exclusive GPU leasing (parallel mode).")
    parser.add_argument("--force-cpu", action="store_true", help="Force CPU execution (slower, for debugging).")
    parser.add_argument("--local-files-only", action="store_true", help="Load models from local cache only (offline mode).")
    parser.add_argument("--hf-cache-dir", default=None, help="Custom Hugging Face cache directory (e.g. /kaggle/temp/hf_cache).")
    parser.add_argument("--refresh-cache", action="store_true", help="Force re-download of model snapshots even if cached.")
    parser.add_argument("--monitor", action="store_true", help="Enable runtime monitoring thread during embedding.")
    parser.add_argument("--save-intermediate", action="store_true", help="Persist intermediate arrays for debugging.")
    parser.add_argument("--quiet", action="store_true", help="Reduce logging verbosity.")
    return parser


# ---------------------------------------------------------------------------
# Main entrypoint
# ---------------------------------------------------------------------------
def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    _configure_logging(args.quiet)

    try:
        chunk_path, output_path = _resolve_paths(args.chunked_dir, args.output_dir)
    except FileNotFoundError:
        return 1

    toggles = _build_feature_toggles(args)
    LOGGER.info(
        "Feature toggles resolved: rerank=%s sparse=%s models=%s",
        toggles.enable_rerank,
        toggles.enable_sparse,
        toggles.sparse_models if toggles.sparse_models else "none",
    )
    print("[embed_v7] Feature toggles resolved. Loading chunks...", flush=True)

    embedder = _build_embedder(args, output_path, toggles)

    try:
        snapshot_path = output_path / "cuda_debug_snapshot.json"
        snapshot_payload = getattr(embedder, "cuda_debug_snapshot", None)
        if snapshot_payload is not None:
            snapshot_path.write_text(json.dumps(snapshot_payload, indent=2), encoding="utf-8")
            LOGGER.info("CUDA debug snapshot saved to %s", snapshot_path)
    except Exception as exc:  # pragma: no cover - filesystem issues
        LOGGER.warning("Failed to persist CUDA debug snapshot: %s", exc)

    LOGGER.info("Loading chunks from %s", chunk_path)
    print(f"[embed_v7] Loading chunks from {chunk_path}...", flush=True)
    load_summary = embedder.load_chunks_from_processing(chunks_dir=str(chunk_path))
    if load_summary.get("error"):
        LOGGER.error("Chunk loading failed: %s", load_summary.get("error"))
        return 1

    total_chunks = load_summary.get("total_chunks_loaded", 0)
    if not total_chunks:
        LOGGER.error("Chunk loading produced zero chunks; verify input dataset under %s", chunk_path)
        return 1

    LOGGER.info(
        "Loaded %s chunks across %s collections",
        total_chunks,
        load_summary.get("collections_loaded", 0),
    )
    print(
        f"[embed_v7] Loaded {total_chunks} chunks across {load_summary.get('collections_loaded', 0)} collections.",
        flush=True,
    )

    LOGGER.info("Running dense ensemble for models: %s", _resolve_ensemble_models(args.ensemble_models))
    print("[embed_v7] Starting dense ensemble...", flush=True)
    dense_results = embedder.generate_embeddings_kaggle_optimized(
        enable_monitoring=args.monitor,
        save_intermediate=args.save_intermediate,
    )
    print("[embed_v7] Dense stage complete.", flush=True)

    if isinstance(dense_results, dict):
        dense_throughput = dense_results.get("chunks_per_second")
        dense_duration = dense_results.get("processing_time_seconds")
        dense_embeddings = dense_results.get("total_embeddings_generated")

        if isinstance(dense_throughput, (int, float)):
            print(
                f"[embed_v7] Dense throughput: {dense_throughput:.2f} chunks/sec",
                flush=True,
            )
        if isinstance(dense_duration, (int, float)):
            print(
                f"[embed_v7] Dense duration: {dense_duration:.2f}s",
                flush=True,
            )
        if isinstance(dense_embeddings, (int, float)):
            print(
                f"[embed_v7] Embeddings generated: {int(dense_embeddings)}",
                flush=True,
            )

    inferred_prefix = args.export_prefix or embedder.get_target_collection_name()
    embedder.export_config.output_prefix = inferred_prefix

    LOGGER.info("Exporting embeddings to %s", embedder.export_config.working_dir)
    print("[embed_v7] Exporting artefacts...", flush=True)
    exported_files = embedder.export_for_local_qdrant()
    LOGGER.info("Export produced %s artefacts", len(exported_files))
    print(f"[embed_v7] Export complete with {len(exported_files)} files.", flush=True)

    summary_path = Path(args.summary_path) if args.summary_path else output_path / f"{inferred_prefix}_processing_summary.json"
    processing_summary = embedder.write_processing_summary(
        summary_path,
        collection_name=inferred_prefix,
        chunk_count=load_summary.get("total_chunks_loaded"),
    )
    LOGGER.info("Processing summary written to %s", summary_path)

    manifest_payload = {
        "chunk_source": str(chunk_path),
        "output_dir": str(output_path),
        "export_prefix": inferred_prefix,
        "ensemble_models": _resolve_ensemble_models(args.ensemble_models),
        "exclusive_mode": not args.disable_exclusive,
        "backend": args.backend,
        "rerank": {
            "enabled": toggles.enable_rerank,
            "model": args.rerank_model,
            "top_k_candidates": args.rerank_candidates,
            "rerank_top_k": args.rerank_top_k,
        },
        "sparse": {
            "enabled": toggles.enable_sparse,
            "models": toggles.sparse_models,
        },
        "feature_toggle_sources": toggles.sources,
        "exported_files": exported_files,
        "dense_results": dense_results,
        "load_summary": load_summary,
        "processing_summary_path": str(summary_path),
        "processing_summary": processing_summary,
        "cuda_debug_snapshot": getattr(embedder, "cuda_debug_snapshot", None),
    }
    manifest_path = _write_manifest(output_path, manifest_payload)
    LOGGER.info("Run manifest written to %s", manifest_path)

    dense_throughput = dense_results.get("chunks_per_second") if isinstance(dense_results, dict) else None
    if isinstance(dense_throughput, (int, float)):
        LOGGER.info("Dense throughput: %.2f chunks/sec", dense_throughput)
    dense_latency = dense_results.get("processing_time_seconds") if isinstance(dense_results, dict) else None
    if isinstance(dense_latency, (int, float)):
        LOGGER.info("Dense stage latency: %.2fs", dense_latency)

    if _in_kaggle():
        kaggle_log = _copy_kaggle_log(output_path, inferred_prefix)
        if kaggle_log is not None:
            LOGGER.info("Kaggle runtime log copied to: %s", kaggle_log)
        else:
            LOGGER.warning(
                "embedding_process.log not found; ensure the embedder initialized successfully before searching for logs."
            )
        LOGGER.info("Original Kaggle log (if present): /kaggle/working/embedding_process.log")
        LOGGER.info("Run artefacts saved under: %s", output_path)
        LOGGER.info("CUDA diagnostics: %s", output_path / "cuda_debug_snapshot.json")

    LOGGER.info("Embedding pipeline complete")
    print("[embed_v7] Embedding pipeline complete.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
