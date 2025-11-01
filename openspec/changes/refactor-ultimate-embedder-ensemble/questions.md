**Task Evaluation**

- **1.1 Review ensemble flow branches**  
  - Benefit: batch_runner.py still mixes three execution styles (primary-only, parallel block starting at ~line 168, sequential block starting at ~line 230, plus the newer `run_exclusive_ensemble`). Mapping every branch clarifies what can be removed before touching code.  
  - Drawback: Time investment only; no functional risk.  
  - Question: Do you know of any downstream callers that still enter `generate_ensemble_embeddings` expecting the parallel block, or should we assume everything has moved to `BatchRunner.run()`?

- **1.2 Inventory EnsembleConfig flags and helpers**  
  - Benefit: `config.py:190-205` still defines deprecated fields, while core.py (e.g., lines 333-371, 664-672) and model_manager.py reference some of them. A full inventory keeps us from deleting something that is still read during startup.  
  - Drawback: Again just effort; prevents accidental regression.  
  - Question: Should we extend the search outside ultimate_embedder (for example CLI scripts in scripts) when auditing field usage?

- **1.3 Confirm CLI entry points and GPU snapshot usage**  
  - Benefit: `core.main()` (lines 1408-1506) still exists, and `kaggle_ultimate_embedder_v4` shim re-exports it. Verifying whether any script calls it lets us remove it safely. Also confirms `controllers.GPUMemorySnapshot.used_bytes` stays private.  
  - Drawback: Minimal—just validation.  
  - Question: Are there scheduled jobs or notebooks that import `core.main()` directly, or is the CLI fully handled via embed_collections_v6.py?

- **2.1 Remove deprecated EnsembleConfig attributes**  
  - Benefit: Fields like `weighting_strategy`, `aggregation_method`, `parallel_encoding`, `memory_efficient`, `sequential_passes`, `preferred_devices`, `warm_cache_after_release` are either unused or duplicative. Removing them shrinks the public surface and prevents misconfiguration (e.g., sequential gating in batch_runner.py).  
  - Drawback: Any external code referencing these attributes will break; we’ll need to update tests (test_exclusive_ensemble_integration.py currently passes `sequential_passes=True`) and demos (`core.main()`).  
  - Question: Is it acceptable to introduce breaking errors for external consumers, or do we need a deprecation cycle where AttributeError messages include migration hints?

- **2.2 Delete parallel/legacy branches in batch runner**  
  - Benefit: The existing parallel block still loads all models simultaneously, undermining the exclusive flow. Removing it aligns execution with `BatchRunner.run()` which already enforces exclusive mode. Also removes complex retry logic now superseded.  
  - Drawback: If any caller still relies on direct parallel execution for performance, we’d regress that use-case.  
  - Question: Do we have any performance benchmarks that mandate keeping a parallel path, or can we fully commit to exclusive mode even if it’s slightly slower?

- **2.3 Excise sparse runtime and dead helpers**  
  - Benefit: `SPARSE_MODELS` and `ModelManager.initialize_sparse_models` exist but nothing downstream consumes `embedder.sparse_models`. Helper methods like `BatchProgressContext.to_dict`, `GPULease.summarize`, `_get_model_primary_dtype`, etc., are unused. Removing them cuts dead code and lowers maintenance.  
  - Drawback: If someone planned to revive sparse runtime soon, we’d have to reintroduce it; also we must adjust any logging/tests expecting these helpers.  
  - Question: Do we have upcoming work that would re-enable sparse runtime, or is it safe to delete now and resurrect later if needed?

- **2.4 Simplify reranker helpers and audit core.main()**  
  - Benefit: Even though the specific helpers (`set_cross_encoder_device`, etc.) aren’t present in the current code, validating their absence and cleaning up `rerank_pipeline` keeps the surface tight. Removing `core.main()` if unused reduces confusion.  
  - Drawback: If marketing/sample notebooks rely on `core.main()`, we’d need to update them simultaneously.  
  - Question: Should we keep a minimal demo entry point elsewhere (e.g., `demo.py`) to replace `core.main()` if we remove it?

- **2.5 Canonicalise KAGGLE_OPTIMIZED_MODELS usage**  
  - Benefit: Multiple modules (model_manager.py, CLI scripts) still allow arbitrary model IDs. Forcing all lookups through `KAGGLE_OPTIMIZED_MODELS` guarantees consistent configs and metadata.  
  - Drawback: Advanced users may want to pass bespoke Hugging Face IDs; we’d need a documented extension path.  
  - Question: Do we need an escape hatch (like a “custom model” flag), or is a strict registry acceptable for all supported workflows?

- **3.1 Exclusive-flow tests**  
  - Benefit: A regression test proving only exclusive leasing runs (e.g., asserting telemetry contains lease events) guards against anyone reintroducing parallel logic.  
  - Drawback: Tests will need GPU mocking or fixtures; could increase runtime.  
  - Question: Should this be an integration test hitting `BatchRunner.run()` or a unit test around `lease_gpus` instrumentation?

- **3.2 Regression tests for removed APIs**  
  - Benefit: Ensures the deleted fields/functions stay gone—import failures or attribute checks will alert us if someone adds them back.  
  - Drawback: Slight maintenance overhead; may annoy developers if the checks are too brittle.  
  - Question: Would you prefer these checks live in pytest (failing tests) or enforced via something like `ruff`/custom lints?

- **3.3 End-to-end smoke run**  
  - Benefit: Validates that after stripping branches and helpers, the embedder still processes a collection—prevents silent runtime regressions.  
  - Drawback: Integration tests are slow and may need GPUs; we might rely on recorded fixtures.  
  - Question: Which smoke test should be the gate—`tests/test_single_collection.py`, TempSmokeTest, or a Kaggle notebook run?

- **3.4 Update docs/CLI notes**  
  - Benefit: Communicates the exclusive-only contract and removal of sparse/parallel modes. Avoids confusion for operators reading `V5_DEPLOYMENT_GUIDE.md` or CLI help.  
  - Drawback: Documentation churn; must keep multiple files in sync (guides, CLI `--help`).  
  - Question: Where should the canonical notice live—EMBED_V6_QUICK_REFERENCE.md, the CLI `--help`, or both?
