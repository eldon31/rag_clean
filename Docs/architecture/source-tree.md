# Source Tree

### Existing Project Structure (Relevant Extract)

```text
processor/
  ultimate_embedder/
    batch_runner.py
    core.py
    gpu_lease.py
    model_manager.py
    rerank_pipeline.py
    sparse_pipeline.py
    telemetry.py
scripts/
  embed_collections_v6.py
docs/
  architecture.md
  ...
```

### New File Organization (Additions Only)

```text
processor/
  ultimate_embedder/
    cross_encoder_executor.py      # New module wrapping rerank batching
    sparse_generator.py            # New module for live sparse inference
  runtime_config.py              # Runtime feature toggles resolver
docs/
  telemetry/
    rerank_sparse_signals.md       # Optional runbook documenting new metrics
```

> Note: Module naming subject to implementation preference; can alternatively live inside existing files if scope small. Primary requirement is keeping responsibilities isolated and testable.

