# Kaggle Embedding Memory Optimization – Fix Summary

## Highlights
- Set the default ensemble roster to `jina-code-embeddings-1.5b` + `bge-m3`, avoiding the flash-attn dependency that broke on Kaggle while keeping higher-quality dual-model coverage.
- Added an `--ensemble-models` CLI override and automatic Kaggle defaults so `python scripts/embed_collections_v5.py` picks up the safe roster without extra flags.
- Hardened ensemble execution by normalizing every encode output to a consistent 2D float32 matrix and trimming row/column mismatches before aggregation; the embedder now logs mitigation events instead of crashing on ragged tensors.
- Recorded mitigation telemetry when a model load fails or dimensions are trimmed, ensuring run summaries capture adaptive behaviour.
- Restored progress bars (`show_progress_bar=True`) so batch execution feedback remains visible during long Kaggle runs.

## Impact
- Kaggle runs no longer fail on `flash_attn` symbol errors or ragged ensemble outputs; sequential batches complete with mitigation notes and full telemetry.
- Operators can still customise ensemble members via CLI, and the runner surfaces the chosen roster in logs and summaries.
- Progress visibility is maintained without sacrificing adaptive GPU management or sequential scheduling features.
