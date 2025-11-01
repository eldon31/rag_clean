## Why
The modular Ultimate Embedder package still carries vestiges of the monolithic build—parallel ensemble paths, dormant sparse pipelines, and partially implemented configuration flags. These leftovers complicate maintenance and hide the true single-model-at-a-time GPU leasing flow that production runs rely on. Aligning the code and specs with the exclusive ensemble design will simplify the control surface and prevent regressions.

## What Changes
- Refactor ensemble execution to rely solely on the exclusive GPU leasing path and delete the parallel/sequential toggle code.
- Trim `EnsembleConfig` to the active fields, drop dormant sparse helpers, and remove dead telemetry/progress utilities.
- Establish `KAGGLE_OPTIMIZED_MODELS` as the authoritative dense model registry across the package and tests.
- Update specs and tests to exercise the exclusive-only ensemble flow and assert the retired APIs stay removed.
- **BREAKING** Remove the sparse runtime exports and deprecated CLI helpers where the API surface allowed them to linger.

## Impact
- Affected specs: embedding-pipeline
- Affected code: processor/ultimate_embedder/*, scripts/embed_collections_v5.py, tests covering ensemble runs
