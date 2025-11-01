# Tech Stack
### Existing Technology Stack
| --- | --- | --- | --- | --- |
| Core Runtime | Python | 3.11 | Maintain | Runtime for embedder, CLI, telemetry integrations. |
| Web/API | FastAPI | Pinned in project | Maintain | Future API exposure of rerank/sparse toggles; no immediate change. |
| Embedding Ensemble | Sentence Transformers | 3.x | Extend | Continue dense models; add CrossEncoder + sparse encoders via same cache dirs. |
| GPU Framework | PyTorch | 2.x | Extend | Enforce leasing + adaptive batching within 12 GB cap across dense, sparse, rerank stages. |
| CLI Orchestration | `embed_collections_v6.py` | V6 | Extend | Defaults rerank/sparse on; CLI exposes `--disable-rerank`/`--disable-sparse` rollback telemetry flags. |
| Export Runtime | Qdrant/FAISS JSONL writers | V4 schema | Extend | Append optional rerank/sparse blocks while keeping legacy keys intact. |
| Sparse Helpers | Custom SPLADE-style pipeline | V5 | Extend | Transition from metadata-only to live sparse inference, honoring keep-list. |

### New Technology Additions

None—enhancements reuse existing dependencies while activating previously scaffolded modules (CrossEncoder reranker, sparse encoders, telemetry hooks).

