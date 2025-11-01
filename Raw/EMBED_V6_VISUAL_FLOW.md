# Embed Collections V6 - Visual Flow Diagram

This document provides visual flowcharts for the complete embedding pipeline.

---

## High-Level System Flow

```
┌─────────────────────────────────────────────────────────┐
│                    START PROGRAM                        │
│                  python embed_v6.py                     │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │  parse_arguments()     │
            │  Detect Environment    │
            │  (Kaggle or Local)     │
            └────────────┬───────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │   Setup Logging        │
            │   - File Handler       │
            │   - Console Handler    │
            └────────────┬───────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│               DISCOVERY PHASE                          │
│                                                        │
│  discover_collections(chunked_dir, max_depth=5)       │
│                                                        │
│  Recursively scan directories:                         │
│  • Find directories with *_chunks.json files           │
│  • Handle name collisions                              │
│  • Build collections map                               │
│                                                        │
│  Output: {"collection_name": Path(...), ...}          │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ Collections │  YES
                  │   Found?    │────────┐
                  └─────────────┘        │
                         │ NO            │
                         ▼               │
                  ┌─────────────┐        │
                  │    ERROR    │        │
                  │   & EXIT    │        │
                  └─────────────┘        │
                                         │
                         ┌───────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │ _filter_collections()  │
            │                        │
            │ If --collections:      │
            │   Filter to requested  │
            │ Else:                  │
            │   Use all discovered   │
            └────────────┬───────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│              INITIALIZATION PHASE                      │
│                                                        │
│  _initialize_embedder(models, exclusive, weights)     │
│                                                        │
│  1. Create EnsembleConfig                              │
│     - model_names: [model1, model2, model3]            │
│     - weights: [0.33, 0.33, 0.34] or custom            │
│     - normalization: "l2"                              │
│                                                        │
│  2. Create KaggleGPUConfig                             │
│     - exclusive_ensemble_mode: True/False              │
│     - max_wait_time: 600s                              │
│     - check_interval: 30s                              │
│                                                        │
│  3. Create KaggleExportConfig                          │
│     - export_format: "qdrant"                          │
│     - output_dir: Path                                 │
│     - enable_validation: True                          │
│                                                        │
│  4. Instantiate UltimateKaggleEmbedderV4               │
│                                                        │
│  Output: embedder instance                             │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│              PROCESSING PHASE                          │
│                                                        │
│  For each collection in filtered_collections:         │
│                                                        │
│    ┌─────────────────────────────────────────┐       │
│    │  process_collection(name, path, ...)    │       │
│    │                                          │       │
│    │  1. Find chunk files                     │       │
│    │  2. Validate chunks exist                │       │
│    │  3. Run embedding job                    │       │
│    │     ├─ EXCLUSIVE MODE (if enabled)       │       │
│    │     │  For each model:                   │       │
│    │     │    - Acquire GPU lease             │       │
│    │     │    - Load model                    │       │
│    │     │    - Generate embeddings           │       │
│    │     │    - Release GPU                   │       │
│    │     │  Combine with weighted average     │       │
│    │                                          │       │
│    │  4. Extract telemetry                    │       │
│    │  5. Log completion                       │       │
│    │  6. Return results dict                  │       │
│    └─────────────────────────────────────────┘       │
│              │                                         │
│              ▼                                         │
│    ┌─────────────────┐                                │
│    │   Success?      │  YES → Store in results        │
│    └─────────────────┘                                │
│              │ NO                                      │
│              ▼                                         │
│         Store in failed_collections                    │
│                                                        │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│              FINALIZATION PHASE                        │
│                                                        │
│  1. _log_processing_summary(results, failed)          │
│     - Log total/success/failure counts                 │
│     - Log failed collection details                    │
│                                                        │
│  2. _export_summary_json(results, file, ...)          │
│     - Create JSON with timestamp                       │
│     - Include all results and failures                 │
│     - Write to output_dir/embedding_summary_v6.json    │
│                                                        │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │   Log "Complete!"      │
            │   EXIT (code 0)        │
            └────────────────────────┘
```

---

## Detailed Discovery Flow

```
discover_collections(chunked_dir, max_depth=5)
│
├─ Validate chunked_dir exists and is directory
│  └─ If not: raise ValueError
│
├─ Initialize: collections = {}, seen_names = set()
│
└─ Call _scan_directory_recursive(chunked_dir, max_depth, ...)
   │
   │  For each entry in directory:
   │  ┌────────────────────────────────────────┐
   │  │                                        │
   │  ▼                                        │
   │  Is entry a directory?                    │
   │  │                                        │
   │  ├─ NO: Skip                              │
   │  │                                        │
   │  └─ YES:                                  │
   │     │                                     │
   │     ▼                                     │
   │     _is_collection_directory(entry)?      │
   │     │                                     │
   │     ├─ YES: FOUND COLLECTION!            │
   │     │  │                                  │
   │     │  ├─ _resolve_collection_name()     │
   │     │  │  • Check if name in seen_names   │
   │     │  │  • If collision:                 │
   │     │  │    Use relative path as name     │
   │     │  │  • Add to seen_names             │
   │     │  │                                  │
   │     │  ├─ collections[name] = entry       │
   │     │  │                                  │
   │     │  └─ Log discovery with chunk count  │
   │     │                                     │
   │     └─ NO: NOT A COLLECTION              │
   │        │                                  │
   │        └─ Recurse deeper:                 │
   │           _scan_directory_recursive(      │
   │              entry,                       │
   │              max_depth,                   │
   │              ...,                         │
   │              current_depth + 1            │
   │           )                               │
   │           │                               │
   │           ├─ Check: current_depth > max_depth?
   │           │  YES: Return (stop recursion) │
   │           │  NO: Continue scanning        │
   │           │                               │
   │           └─ (Repeat for subdirectories)  │
   │                                           │
   └───────────────────────────────────────────┘

Return collections dictionary
```

---

## Collection Processing Detail

```
process_collection(name, path, embedder, args)
│
├─ Log header: "Processing collection: {name}"
│  Log mode: EXCLUSIVE or PARALLEL
│
├─ find_chunk_files(path)
│  └─ Returns: List[Path] of *_chunks.json files
│
├─ Validate chunk files exist
│  └─ If empty: return {}
│
├─ Log: "Found N chunk files"
│
└─ embedder.generate_embeddings_kaggle_optimized(
      enable_monitoring=True,
      save_intermediate=True
   )
   │
   ├─ batch_runner.run() detects exclusive_mode
   │  └─ Calls batch_runner.run_exclusive_ensemble()
   │
   ├─ EXCLUSIVE MODE (ONLY MODE - args.exclusive_ensemble = True):
   │  │
   │  │  models = ["model1", "model2", "model3"]
   │  │  all_embeddings = []
   │  │
   │  │  For each model in models:
   │  │  ┌──────────────────────────────────────┐
   │  │  │                                      │
   │  │  │  1. GPU_LEASE.acquire(model)        │
   │  │  │     └─ Wait for T4 GPU availability  │
   │  │  │     └─ Log lease event: "acquire"    │
   │  │  │                                      │
   │  │  │  2. Load model to GPU                │
   │  │  │     • Enable DataParallel mode       │
   │  │  │     • GPU memory limit: 12GB/GPU     │
   │  │  │     model = SentenceTransformer(     │
   │  │  │         model_name,                  │
   │  │  │         device="cuda"                │
   │  │  │     )                                │
   │  │  │     if torch.cuda.device_count() > 1:│
   │  │  │       model = DataParallel(model)    │
   │  │  │       torch.cuda.set_per_process_    │
   │  │  │         memory_fraction(0.75)  # 12GB│
   │  │  │                                      │
   │  │  │  3. Generate embeddings              │
   │  │  │     For each chunk_file:             │
   │  │  │       │                              │
   │  │  │       ├─ Log throughput START:       │
   │  │  │       │  • Model: {model_name}       │
   │  │  │       │  • File: {chunk_file_name}   │
   │  │  │       │  • Chunks: {num_chunks}      │
   │  │  │       │  • Timestamp: {start_time}   │
   │  │  │       │  • GPUs: {gpu_count}         │
   │  │  │       │  • Batch size/GPU: {batch}   │
   │  │  │       │                              │
   │  │  │       ├─ For each chunk in file:     │
   │  │  │       │    embedding = model.encode( │
   │  │  │       │        chunk["text"],        │
   │  │  │       │        batch_size=batch_size │
   │  │  │       │    )  # Distributed across   │
   │  │  │       │       # GPUs via DataParallel│
   │  │  │       │    all_embeddings.append(    │
   │  │  │       │        embedding             │
   │  │  │       │    )                         │
   │  │  │       │                              │
   │  │  │       └─ Log throughput END:         │
   │  │  │          • Chunks processed: {count} │
   │  │  │          • Duration: {elapsed}s      │
   │  │  │          • Rate: {chunks/sec}        │
   │  │  │          • GPU memory used: {mem}GB  │
   │  │  │          • Timestamp: {end_time}     │
   │  │  │                                      │
   │  │  │  4. Unload model from GPU            │
   │  │  │     del model                        │
   │  │  │     torch.cuda.empty_cache()         │
   │  │  │                                      │
   │  │  │  5. GPU_LEASE.release(model)         │
   │  │  │     └─ Log lease event: "release"    │
   │  │  │                                      │
   │  │  └──────────────────────────────────────┘
   │  │
   │  │  6. Combine embeddings:
   │  │     ensemble_embedding = weighted_avg(
   │  │         all_embeddings,
   │  │         weights=[0.33, 0.33, 0.34]
   │  │     )
   │  │
   │  │  7. Normalize: L2 normalization
   │  │
   │  │  8. Store in Qdrant:
   │  │     For each chunk, embedding:
   │  │       qdrant.upsert(
   │  │           collection_name=name,
   │  │           points=[{
   │  │               "id": chunk_id,
   │  │               "vector": ensemble_embedding,
   │  │               "payload": {
   │  │                   "text": chunk_text,
   │  │                   "metadata": {...}
   │  │               }
   │  │           }]
   │  │       )
   │  │
   │  └─ Return: {
   │       "models_executed": ["model1", "model2", "model3"],
   │       "lease_events": [
   │           {"event_type": "acquire", "model": "model1", ...},
   │           {"event_type": "release", "model": "model1", ...},
   │           ...
   │       ],
   │       "total_embeddings_generated": 1000,
   │       "qdrant_collection": "Docling"
   │     }
```

---

## Function Call Tree

```
main()
│
├─── parse_arguments()
│    └─── Returns: Namespace with all args
│
├─── logging.basicConfig(...)
│
├─── discover_collections(chunked_dir, max_depth)
│    │
│    └─── _scan_directory_recursive(directory, max_depth, ...)
│         │
│         ├─── _is_collection_directory(entry)
│         │    └─── Returns: bool
│         │
│         └─── _resolve_collection_name(entry, chunked_dir, seen_names)
│              └─── Returns: str (unique name)
│
├─── _filter_collections(all_collections, args.collections)
│    └─── Returns: dict[str, Path] (filtered)
│
├─── _initialize_embedder(args.ensemble_models, args.exclusive_ensemble, args.ensemble_weights)
│    │
│    ├─── EnsembleConfig(...)
│    ├─── KaggleGPUConfig(...)
│    ├─── KaggleExportConfig(...)
│    └─── UltimateKaggleEmbedderV4(...)
│         └─── Returns: embedder instance
│
├─── For each collection:
│    │
│    └─── process_collection(name, path, embedder, args)
│         │
│         ├─── find_chunk_files(path)
│         │    └─── Returns: List[Path]
│         │
│         ├─── embedder.load_chunks_from_processing(chunks_dir)
│         │    └─── Returns: load_summary
│         │
│         ├─── embedder.generate_embeddings_kaggle_optimized(...)
│         │    │
│         │    └─── batch_runner.run(enable_monitoring, save_intermediate)
│         │         │
│         │         └─── batch_runner.run_exclusive_ensemble()
│         │              └─── Returns: dict (results with telemetry)
│         │
│         ├─── _extract_telemetry(results)
│         │    └─── Returns: (models, events, count)
│         │
│         └─── _log_collection_completion(name, models, events, count, exclusive)
│
├─── _log_processing_summary(results, failed_collections)
│
└─── _export_summary_json(results, output_file, models, exclusive)
```

---

## Data Structure Flow

### Input Data Structure

```python
# Directory structure on disk:
Chunked/
├── Docling/
│   ├── intro_chunks.json          # {"chunks": [...]}
│   └── tutorial_chunks.json       # {"chunks": [...]}
└── FAST_DOCS/
    └── fastapi_fastapi/
        └── docs_chunks.json       # {"chunks": [...]}

# Each *_chunks.json file contains:
{
    "doc_id": "intro",
    "chunks": [
        {
            "chunk_id": "intro_chunk_0",
            "text": "This is the introduction...",
            "metadata": {
                "source": "intro.md",
                "section": "Overview"
            }
        },
        {
            "chunk_id": "intro_chunk_1",
            "text": "Next section content...",
            "metadata": {...}
        }
    ]
}
```

### Intermediate Data Structures

```python
# After discover_collections():
collections = {
    "Docling": Path("Chunked/Docling"),
    "FAST_DOCS_fastapi_fastapi": Path("Chunked/FAST_DOCS/fastapi_fastapi")
}

# After _filter_collections():
filtered = {
    "Docling": Path("Chunked/Docling")  # If --collections Docling specified
}

# After _initialize_embedder():
embedder = UltimateKaggleEmbedderV4(
    ensemble_config=EnsembleConfig(...),
    gpu_config=KaggleGPUConfig(...),
    export_config=KaggleExportConfig(...)
)

# During process_collection():
chunk_files = [
    Path("Chunked/Docling/intro_chunks.json"),
    Path("Chunked/Docling/tutorial_chunks.json")
]

# After embedder.generate_embeddings_kaggle_optimized():
# (called via batch_runner.run() -> run_exclusive_ensemble())
results = {
    "models_executed": [
        "sentence-transformers/all-MiniLM-L6-v2",
        "BAAI/bge-small-en-v1.5",
        "nomic-ai/nomic-embed-text-v1.5"
    ],
    "lease_events": [
        {
            "event_type": "acquire",
            "model": "sentence-transformers/all-MiniLM-L6-v2",
            "timestamp": "2025-10-22T14:30:10.123456"
        },
        {
            "event_type": "release",
            "model": "sentence-transformers/all-MiniLM-L6-v2",
            "timestamp": "2025-10-22T14:31:25.789012"
        }
        # ... more events
    ],
    "total_embeddings_generated": 1000,
    "qdrant_collection": "Docling",
    "processing_time": 235.4
}
```

### Output Data Structures

```python
# In Qdrant (vector database):
{
    "collection_name": "Docling",
    "vectors_count": 1000,
    "points": [
        {
            "id": "intro_chunk_0",
            "vector": [0.123, -0.456, 0.789, ...],  # 384 dimensions
            "payload": {
                "text": "This is the introduction...",
                "chunk_id": "intro_chunk_0",
                "doc_id": "intro",
                "metadata": {
                    "source": "intro.md",
                    "section": "Overview"
                }
            }
        }
        # ... 999 more points
    ]
}

# In embedding_summary_v6.json:
{
    "timestamp": "2025-10-22T14:35:22.123456",
    "environment": "Kaggle",
    "ensemble_models": [...],
    "exclusive_ensemble_mode": true,
    "results": {
        "Docling": {
            "models_executed": [...],
            "lease_events": [...],
            "total_embeddings_generated": 1000,
            "qdrant_collection": "Docling"
        }
    },
    "failed_collections": {}
}
```

---

## Timeline: Exclusive Mode (Only Mode)

### Exclusive Mode (Sequential) - Model-at-a-Time

```
Time →
0s     ┌──────────────────────────────────────────────────┐
       │ Start: Process Collection "Docling"              │
       │ (Exclusive mode - ONLY execution path)           │
       └──────────────────────────────────────────────────┘
10s    │
       ├─ [GPU LEASE ACQUIRE] model1
       │
30s    ├─ Load model1 to GPU
       │
45s    ├─ Generate embeddings with model1
       │  (process all chunks)
       │
75s    ├─ Unload model1
       │
80s    ├─ [GPU LEASE RELEASE] model1
       │
       ├─ [GPU LEASE ACQUIRE] model2
       │
100s   ├─ Load model2 to GPU
       │
115s   ├─ Generate embeddings with model2
       │
145s   ├─ Unload model2
       │
150s   ├─ [GPU LEASE RELEASE] model2
       │
       ├─ [GPU LEASE ACQUIRE] model3
       │
170s   ├─ Load model3 to GPU
       │
185s   ├─ Generate embeddings with model3
       │
215s   ├─ Unload model3
       │
220s   ├─ [GPU LEASE RELEASE] model3
       │
225s   ├─ Combine ensemble (weighted average)
       │
230s   ├─ Store in Qdrant
       │
235s   └─ ✅ Complete

Total: 235 seconds
GPU Usage: One model at a time (low memory, safer)
Benefits: ✅ Works on all GPU types, optimal VRAM management
Status: ✅ PRODUCTION READY - Parallel mode removed in V6.1
```

### 📝 Architecture Simplification Note

**Previous Version (V6.0):** Supported both parallel and exclusive modes
**Current Version (V6.1):** Exclusive mode only (445 lines of parallel code removed)

**Rationale:**
- Parallel mode had zero test coverage
- High OOM risk on Kaggle T4x2 GPUs
- Exclusive mode provides better VRAM management
- Single execution path improves maintainability

---

## Error Handling Flow

```
Try Block:
├─ discover_collections()
│  ├─ ValueError: chunked_dir doesn't exist
│  │  └─ Log error → Exit
│  │
│  └─ OSError/PermissionError in subdirectory
│     └─ Log warning → Continue (skip directory)
│
├─ _filter_collections()
│  └─ ValueError: requested collections not found
│     └─ Log error → Exit
│
├─ _initialize_embedder()
│  └─ Exception: embedder initialization failed
│     └─ Raise RuntimeError → Log error → Exit
│
└─ process_collection() for each collection:
   ├─ Exception during processing
   │  └─ Catch → Store in failed_collections → Continue
   │
   └─ RuntimeError: invalid results structure
      └─ Catch → Store in failed_collections → Continue

Finalization:
├─ _log_processing_summary()
│  └─ Logs all failures with exception types
│
└─ _export_summary_json()
   ├─ IOError: can't write JSON file
   │  └─ Log error → Continue (non-fatal)
   │
   └─ Success → Log file path → Exit
```

---

## Memory Management Flow (Exclusive Mode)

```
Collection Processing Loop:
│
├─ Collection 1: "Docling"
│  │
│  ├─ Model 1:
│  │  ├─ Load to GPU: +2GB VRAM
│  │  ├─ Generate embeddings: +1GB VRAM (batches)
│  │  ├─ Unload: torch.cuda.empty_cache()
│  │  └─ GPU memory released: -3GB VRAM
│  │
│  ├─ Model 2:
│  │  ├─ Load to GPU: +2.5GB VRAM
│  │  ├─ Generate embeddings: +1GB VRAM
│  │  ├─ Unload: torch.cuda.empty_cache()
│  │  └─ GPU memory released: -3.5GB VRAM
│  │
│  └─ Model 3:
│     ├─ Load to GPU: +2.8GB VRAM
│     ├─ Generate embeddings: +1GB VRAM
│     ├─ Unload: torch.cuda.empty_cache()
│     └─ GPU memory released: -3.8GB VRAM
│
│  Peak GPU Usage: ~4GB (single model + batches)
│  ✅ Fits in Kaggle T4 (16GB)
│  ✅ DEFAULT BEHAVIOR (safest option)
│
└─ Collection 2: "FAST_DOCS"
   └─ (Repeat same pattern)

Key Advantages:
• GPU memory reused for each model sequentially
• Prevents OOM errors on all GPU types
• Only execution mode in V6.1 (parallel mode removed)
• Optimal VRAM management for Kaggle T4x2 and other GPUs
```

---

## Summary Table: Function Responsibilities

| Function | Module | Input | Output | Side Effects |
|----------|--------|-------|--------|--------------|
| `_is_collection_directory` | Discovery | Path | bool | Logs warnings |
| `_resolve_collection_name` | Discovery | Path, Path, set | str | None |
| `_scan_directory_recursive` | Discovery | Path, int, dict, set | None | Modifies dict/set, logs |
| `discover_collections` | Discovery | Path, int | dict[str, Path] | Logs, raises |
| `_get_ensemble_mode_label` | Processing | bool | str | None |
| `_extract_telemetry` | Processing | dict | tuple | None |
| `_log_collection_completion` | Processing | str, list, list, int, bool | None | Logs |
| `process_collection` | Processing | str, Path, Embedder, args | dict | Logs, GPU ops, raises |
| `_filter_collections` | Orchestration | dict, list | dict | Raises |
| `_initialize_embedder` | Orchestration | list, bool, list | Embedder | Raises |
| `_log_processing_summary` | Orchestration | dict, dict | None | Logs |
| `_export_summary_json` | Orchestration | dict, Path, list, bool | None | Writes file, logs |
| `main` | Orchestration | None | None | All side effects |
| `parse_arguments` | Parsing | None | Namespace | None |

---

## Conclusion

These visual diagrams show the complete flow of `embed_collections_v6.py` from command-line invocation to final outputs. The modular architecture with 13 helper functions ensures:

1. **Clear separation of concerns**: Each function has a single, well-defined purpose
2. **Testability**: All helpers can be unit tested independently
3. **Maintainability**: Visual flow makes understanding and modifications easier
4. **Debugging**: Structured logging at each phase aids troubleshooting
5. **Performance**: Exclusive mode manages GPU memory efficiently for all environments

**V6.1 Update (October 23, 2025):**
- Parallel mode completely removed (445 lines)
- Exclusive mode is now the only execution path
- Simplified architecture improves maintainability
- ThroughputMonitor extracted to separate module

Ready for production deployment! 🚀
