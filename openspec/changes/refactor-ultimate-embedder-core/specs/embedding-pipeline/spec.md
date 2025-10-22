## ADDED Requirements
### Requirement: Componentised Embedder Runtime
The Kaggle embedder facade (`processor/ultimate_embedder/core.py`) SHALL delegate chunk ingestion, model lifecycle, adaptive batching, sparse/rerank pipelines, monitoring, and export coordination to dedicated runtime modules under `processor/ultimate_embedder/`, ensuring each module is independently testable and no single file exceeds 800 executable lines.

#### Scenario: Facade orchestrates services
- **WHEN** `UltimateKaggleEmbedderV4.generate_embeddings_kaggle_optimized()` runs
- **THEN** chunk batches flow from the loader module, embeddings execute through the batch runner, telemetry is captured by the monitoring helpers, and exports are produced by the export coordinator without duplicating their logic in `core.py`.

#### Scenario: Modules independently testable
- **GIVEN** unit tests import the chunk loader, model manager, batch runner, sparse pipeline, and rerank pipeline modules in isolation
- **WHEN** the tests execute their public APIs
- **THEN** the modules operate without requiring the full `UltimateKaggleEmbedderV4` facade, enabling focused regression coverage.

#### Scenario: Maintainability threshold enforced
- **WHEN** the refactor completes
- **THEN** `processor/ultimate_embedder/core.py` contains fewer than 800 lines of executable code (excluding comments/docstrings), demonstrating that responsibilities moved into the dedicated modules.

#### Scenario: Automated guardrails prevent regression
- **GIVEN** the executable-line checker runs as part of CI/tooling
- **WHEN** a change causes `processor/ultimate_embedder/core.py` to exceed the 800-line ceiling
- **THEN** the checker fails the build, blocking the regression until the file is reduced or responsibilities move into the dedicated modules.
