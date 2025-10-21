## ADDED Requirements

### Requirement: Modular Embedder Architecture
The embedding pipeline SHALL expose the Kaggle embedder as a modular package that separates configuration, controllers, telemetry, core orchestration, and export responsibilities into dedicated modules while preserving the existing public API (`UltimateKaggleEmbedderV4`, `generate_embeddings_kaggle_optimized`). The legacy monolithic module MUST re-export the new components until downstream consumers migrate so that batch runner scripts continue functioning without code changes.

#### Scenario: Legacy import path still works
- **GIVEN** an external script imports `UltimateKaggleEmbedderV4` from `processor.kaggle_ultimate_embedder_v4`
- **WHEN** the modularised package is released
- **THEN** the import resolves successfully and the embedder can execute ensemble rotations without behavioural regressions

#### Scenario: Modular package available for direct use
- **GIVEN** a developer imports modules from `processor.ultimate_embedder`
- **WHEN** they access configuration classes, controllers, or export helpers
- **THEN** the modules provide stable, documented interfaces that mirror the functionality previously embedded in the monolithic file

#### Scenario: Legacy shim deprecation window
- **GIVEN** downstream consumers still import from `processor.kaggle_ultimate_embedder_v4`
- **WHEN** the modular package ships
- **THEN** the shim remains supported, with deprecation notices only after at least one minor release cycle, so teams have time to migrate to the new module paths
