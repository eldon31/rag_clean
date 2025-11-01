# Embed Collections V6.1 - Architecture Documentation

**File:** `scripts/embed_collections_v6.py`  
**Purpose:** Production-grade ensemble embedding pipeline with exclusive GPU lease support  
**Last Updated:** October 23, 2025  
**Version:** V6.1 - Simplified Architecture (Parallel Mode Removed)

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Data Flow](#data-flow)
4. [Module Reference](#module-reference)
5. [Function Specifications](#function-specifications)
6. [Output Specifications](#output-specifications)
7. [Usage Examples](#usage-examples)

---

## System Overview

`embed_collections_v6.py` is a CLI tool that orchestrates the embedding of document collections using ensemble models with Qdrant vector database integration. It supports both local and Kaggle environments with automatic environment detection.

### Key Features

- **Recursive Collection Discovery**: Finds collections at any nesting depth (up to 5 levels)
- **Exclusive GPU Mode**: Sequential model execution with GPU lease management - ONLY MODE ✅
- **Environment Aware**: Automatic detection and configuration for Kaggle vs Local
- **Comprehensive Logging**: Detailed telemetry including GPU lease events
- **Fault Tolerant**: Continues processing after collection failures
- **Structured Output**: JSON summary with results and metadata
- **Throughput Monitoring**: Extracted to dedicated module for clean architecture

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         EMBED COLLECTIONS V6                        │
│                     CLI Entry Point (main)                          │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────────┐
        │   PHASE 1: INITIALIZATION & DISCOVERY          │
        └────────────────────────────────────────────────┘
                                 │
        ┌────────────────────────┴────────────────────────┐
        │                                                  │
        ▼                                                  ▼
┌──────────────────┐                          ┌──────────────────────┐
│ parse_arguments  │                          │ Setup Logging        │
│                  │                          │ - File handler       │
│ Input:           │                          │ - Stream handler     │
│ - sys.argv       │                          │ - Log level          │
│                  │                          └──────────────────────┘
│ Output:          │                                     │
│ - Namespace args │                                     │
│   • chunked_dir  │                                     │
│   • output_dir   │                                     │
│   • collections  │                                     │
│   • ensemble_*   │                                     │
│   • batch_size   │                                     │
│   • verbose      │                                     │
└──────────────────┘                                     │
        │                                                 │
        └─────────────────┬───────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────────────┐
        │   discover_collections(chunked_dir, max_depth)  │
        │                                                 │
        │   ┌──────────────────────────────────────┐    │
        │   │ _scan_directory_recursive            │    │
        │   │                                      │    │
        │   │  For each directory entry:           │    │
        │   │    ├─ Is directory?                  │    │
        │   │    │                                 │    │
        │   │    ├─ _is_collection_directory?      │    │
        │   │    │  YES: Add to collections        │    │
        │   │    │       ├─ _resolve_collection_   │    │
        │   │    │       │   name (handle          │    │
        │   │    │       │   collisions)           │    │
        │   │    │       └─ Log discovery          │    │
        │   │    │                                 │    │
        │   │    └─ NO: Recurse if depth < max    │    │
        │   └──────────────────────────────────────┘    │
        │                                                 │
        │   Output: dict[str, Path]                      │
        │   Example: {                                   │
        │     "Docling": Path("Chunked/Docling"),       │
        │     "FAST_DOCS_fastapi": Path(...)            │
        │   }                                            │
        └─────────────────────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────────────┐
        │   _filter_collections(all, requested)           │
        │                                                 │
        │   If requested is None:                         │
        │     return all_collections                      │
        │   Else:                                         │
        │     validate requested exist                    │
        │     return filtered subset                      │
        │                                                 │
        │   Output: dict[str, Path] (filtered)           │
        └─────────────────────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────────────┐
        │              PHASE 2: EMBEDDER SETUP            │
        └─────────────────────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────────────┐
        │   _initialize_embedder(models, exclusive, wts)  │
        │                                                 │
        │   Creates:                                      │
        │   ┌────────────────────────────────────┐       │
        │   │ EnsembleConfig                     │       │
        │   │ - model_names: List[str]           │       │
        │   │ - weights: List[float]             │       │
        │   │ - normalization: "l2"              │       │
        │   └────────────────────────────────────┘       │
        │              ▼                                  │
        │   ┌────────────────────────────────────┐       │
        │   │ KaggleGPUConfig                    │       │
        │   │ - exclusive_ensemble_mode: bool    │       │
        │   │ - max_wait_time: 600s              │       │
        │   │ - check_interval: 30s              │       │
        │   └────────────────────────────────────┘       │
        │              ▼                                  │
        │   ┌────────────────────────────────────┐       │
        │   │ KaggleExportConfig                 │       │
        │   │ - export_format: "qdrant"          │       │
        │   │ - output_dir: Path                 │       │
        │   │ - enable_validation: True          │       │
        │   └────────────────────────────────────┘       │
        │              ▼                                  │
        │   ┌────────────────────────────────────┐       │
        │   │ UltimateKaggleEmbedderV4           │       │
        │   │ - device: "cuda"                   │       │
        │   │ - qdrant_host: str                 │       │
        │   │ - qdrant_port: int                 │       │
        │   └────────────────────────────────────┘       │
        │                                                 │
        │   Output: UltimateKaggleEmbedderV4 instance    │
        └─────────────────────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────────────┐
        │           PHASE 3: COLLECTION PROCESSING        │
        └─────────────────────────────────────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │ For each collection in filtered:  │
        └─────────────────┬─────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────────────┐
        │   process_collection(name, path, embedder, args)│
        │                                                 │
        │   1. Find chunk files                           │
        │      └─ find_chunk_files(collection_dir)        │
        │         Output: List[Path]                      │
        │                                                 │
        │   2. Validate chunk files exist                 │
        │      └─ If empty: return {}                     │
        │                                                 │
        │   3. Run embedding job                          │
        │      └─ embedder.generate_embeddings_kaggle_optimized() │
        │         │                                       │
        │         └─ batch_runner.run()                   │
        │            │                                    │
        │            └─ batch_runner.run_exclusive_ensemble() │
        │                                                 │
        │         ┌──────────────────────────────┐       │
        │         │ EXCLUSIVE MODE (ONLY MODE)    │       │
        │         │                               │       │
        │         │ For each model:               │       │
        │         │   ├─ Acquire GPU lease        │       │
        │         │   ├─ Load model to GPU        │       │
        │         │   ├─ Generate embeddings      │       │
        │         │   ├─ Release GPU lease        │       │
        │         │   └─ Log lease event          │       │
        │         │                               │       │
        │         │ Combine: weighted average     │       │
        │         └──────────────────────────────┘       │
        │                                                 │
        │   4. Extract telemetry                          │
        │      └─ _extract_telemetry(results)             │
        │         Output: (models, events, count)         │
        │                                                 │
        │   5. Log completion                             │
        │      └─ _log_collection_completion(...)         │
        │                                                 │
        │   Output: dict {                                │
        │     "models_executed": ["model1", ...],        │
        │     "lease_events": [{...}],                   │
        │     "total_embeddings_generated": int,         │
        │     "qdrant_collection": str                   │
        │   }                                            │
        └─────────────────────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────────────┐
        │   Collect results & failures                    │
        │                                                 │
        │   results: dict[str, dict]                      │
        │   failed_collections: dict[str, Exception]      │
        └─────────────────────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────────────┐
        │              PHASE 4: FINALIZATION              │
        └─────────────────────────────────────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
┌──────────────────────┐      ┌──────────────────────────┐
│ _log_processing_     │      │ _export_summary_json     │
│ summary(results,     │      │ (results, output_file,   │
│ failed)              │      │ models, exclusive)       │
│                      │      │                          │
│ Logs:                │      │ Creates JSON:            │
│ - Total count        │      │ {                        │
│ - Success count      │      │   "timestamp": str,      │
│ - Failure count      │      │   "environment": str,    │
│ - Failed details     │      │   "ensemble_models": [], │
│                      │      │   "exclusive_mode": bool,│
└──────────────────────┘      │   "results": {},         │
                               │   "failed": {}           │
                               │ }                        │
                               │                          │
                               │ File: embedding_summary_ │
                               │       v6.json            │
                               └──────────────────────────┘
                                          │
                                          ▼
                               ┌──────────────────────┐
                               │   COMPLETE           │
                               │   Exit code: 0       │
                               └──────────────────────┘
```

---

## Data Flow

### Input → Output Transformation

```
INPUT STAGE
───────────
├─ Command Line Arguments
│  └─ python scripts/embed_collections_v6.py --exclusive_ensemble
│
├─ Chunked Directory Structure
│  └─ Chunked/
│     ├─ Docling/
│     │  ├─ doc1_chunks.json
│     │  └─ doc2_chunks.json
│     ├─ FAST_DOCS/
│     │  └─ fastapi_fastapi/
│     │     └─ doc_chunks.json
│     └─ Qdrant/
│        └─ qdrant_documentation/
│           └─ documentation/
│              └─ doc_chunks.json

▼ TRANSFORMATION STAGE
─────────────────────
├─ Discovery Phase
│  └─ Collections Map: {"Docling": Path(...), ...}
│
├─ Filtering Phase
│  └─ Filtered Collections: {"Docling": Path(...)}
│
├─ Embedding Phase
│  ├─ For each collection:
│  │  ├─ Load chunks → List[Dict]
│  │  ├─ Generate embeddings → np.ndarray
│  │  ├─ Combine ensemble → np.ndarray (averaged)
│  │  └─ Store in Qdrant → Collection created
│  │
│  └─ Telemetry: {models_executed, lease_events, count}

▼ OUTPUT STAGE
─────────────
├─ Qdrant Collections (Vector Database)
│  ├─ Collection: "Docling"
│  │  ├─ Vectors: 384-dim ensemble embeddings
│  │  ├─ Payloads: {text, metadata, chunk_id}
│  │  └─ Count: N points
│  │
│  └─ Collection: "FAST_DOCS_fastapi"
│     └─ ... (similar structure)
│
├─ Log Files
│  └─ output_dir/embedding_v6.log
│     ├─ Timestamp: 2025-10-22 14:30:00
│     ├─ Discovery: Found 224 collections
│     ├─ Processing: Collection "Docling" started
│     ├─ GPU Lease: Acquired for model1
│     ├─ GPU Lease: Released for model1
│     ├─ Completion: ✅ Docling (1000 embeddings)
│     └─ Summary: 224/224 succeeded
│
└─ JSON Summary
   └─ output_dir/embedding_summary_v6.json
      {
        "timestamp": "2025-10-22T14:35:22",
        "environment": "Kaggle",
        "ensemble_models": [
          "sentence-transformers/all-MiniLM-L6-v2",
          "BAAI/bge-small-en-v1.5",
          "nomic-ai/nomic-embed-text-v1.5"
        ],
        "exclusive_ensemble_mode": true,
        "results": {
          "Docling": {
            "models_executed": ["model1", "model2", "model3"],
            "lease_events": [
              {"event_type": "acquire", "model": "model1", "timestamp": "..."},
              {"event_type": "release", "model": "model1", "timestamp": "..."}
            ],
            "total_embeddings_generated": 1000,
            "qdrant_collection": "Docling"
          }
        },
        "failed_collections": {}
      }
```

---

## Module Reference

### Constants Module

```python
# File Pattern Recognition
CHUNK_FILE_PATTERN = "*_chunks.json"        # Identifies collection directories
MAX_DISCOVERY_DEPTH = 5                      # Maximum recursion depth

# Result Dictionary Keys (API contract)
RESULT_KEY_MODELS_EXECUTED = "models_executed"
RESULT_KEY_LEASE_EVENTS = "lease_events"
RESULT_KEY_TOTAL_EMBEDDINGS = "total_embeddings_generated"

# Embedder Configuration
DEFAULT_FALLBACK_MODEL = "nomic-ai/nomic-embed-text-v1.5"
DEFAULT_ENSEMBLE_MODELS = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "BAAI/bge-small-en-v1.5", 
    "nomic-ai/nomic-embed-text-v1.5"
]
```

### Helper Functions Hierarchy

```
embed_collections_v6.py
│
├─ DISCOVERY MODULE
│  ├─ _is_collection_directory(directory) → bool
│  ├─ _resolve_collection_name(dir, base, seen) → str
│  ├─ _scan_directory_recursive(...) → None (modifies dict)
│  └─ discover_collections(chunked_dir, max_depth) → dict[str, Path]
│
├─ PROCESSING MODULE
│  ├─ _get_ensemble_mode_label(exclusive) → str
│  ├─ _extract_telemetry(results) → tuple[list, list, int]
│  ├─ _log_collection_completion(...) → None
│  └─ process_collection(name, path, embedder, args) → dict
│
├─ ORCHESTRATION MODULE
│  ├─ _filter_collections(all, requested) → dict[str, Path]
│  ├─ _initialize_embedder(models, exclusive, weights) → Embedder
│  ├─ _log_processing_summary(results, failed) → None
│  ├─ _export_summary_json(results, file, models, exclusive) → None
│  └─ main() → None
│
└─ ARGUMENT PARSING
   └─ parse_arguments() → Namespace
```

---

## Function Specifications

### 1. Discovery Module

#### `_is_collection_directory(directory: Path) -> bool`

**Purpose:** Determine if a directory contains chunk files (non-recursive check).

**Algorithm:**
```python
1. Try to glob for CHUNK_FILE_PATTERN in directory
2. If OSError/PermissionError: log warning, return False
3. Return True if any chunk files found, else False
```

**Input:**
- `directory`: Path object to check

**Output:**
- `True`: Directory contains at least one `*_chunks.json` file
- `False`: No chunk files found or directory inaccessible

**Example:**
```python
# Directory structure:
# Chunked/Docling/
#   ├─ intro_chunks.json
#   └─ tutorial_chunks.json

_is_collection_directory(Path("Chunked/Docling"))
# Returns: True

_is_collection_directory(Path("Chunked/EmptyDir"))
# Returns: False
```

**Expected Log Output:**
```
# Success case: No logs (silent success)

# Error case:
WARNING - Cannot access directory /path/to/restricted: Permission denied
```

---

#### `_resolve_collection_name(collection_dir: Path, chunked_dir: Path, seen_names: set[str]) -> str`

**Purpose:** Generate unique collection name, handling collisions.

**Algorithm:**
```python
1. Extract base name from collection_dir
2. If base_name not in seen_names:
     return base_name
3. Else (collision detected):
     try:
       compute relative_path from chunked_dir
       return relative_path with separators replaced by "_"
     except ValueError:
       compute MD5 hash of path
       return f"{base_name}_{hash[:8]}"
```

**Input:**
- `collection_dir`: Path to collection directory
- `chunked_dir`: Base directory for relative path calculation
- `seen_names`: Set of already-used collection names

**Output:**
- Unique collection name string

**Example:**
```python
# Scenario 1: No collision
_resolve_collection_name(
    Path("Chunked/Docling"),
    Path("Chunked"),
    seen_names=set()
)
# Returns: "Docling"

# Scenario 2: Collision with nested structure
_resolve_collection_name(
    Path("Chunked/FAST_DOCS/fastapi/fastapi"),
    Path("Chunked"),
    seen_names={"fastapi"}  # Collision!
)
# Returns: "FAST_DOCS_fastapi_fastapi"

# Scenario 3: Fallback to hash
_resolve_collection_name(
    Path("/completely/different/path"),
    Path("Chunked"),
    seen_names=set()
)
# Returns: "path_a3f5c8d1" (hash-based)
```

---

#### `_scan_directory_recursive(...) -> None`

**Purpose:** Recursively traverse directories to find collections (modifies collections dict in-place).

**Algorithm:**
```python
1. Check current_depth ≤ max_depth, else return
2. Validate directory exists and is a directory
3. Try to list directory entries
4. For each entry:
     if entry.is_dir():
       if _is_collection_directory(entry):
         # Found collection!
         name = _resolve_collection_name(entry, chunked_dir, seen_names)
         collections[name] = entry
         seen_names.add(name)
         log discovery with chunk count
       else:
         # Recurse deeper
         _scan_directory_recursive(entry, ..., current_depth + 1)
```

**Input:**
- `directory`: Current directory being scanned
- `max_depth`: Maximum recursion limit
- `chunked_dir`: Base directory for name resolution
- `collections`: Dictionary to populate (modified in-place)
- `seen_names`: Set of used names (modified in-place)
- `current_depth`: Current recursion level (default 0)

**Output:**
- None (modifies `collections` and `seen_names` in-place)

**Side Effects:**
- Adds entries to `collections` dict
- Adds entries to `seen_names` set
- Logs INFO messages for each discovered collection
- Logs WARNING messages for access errors

**Example:**
```python
# Directory structure:
# Chunked/
#   ├─ Docling/
#   │  └─ doc_chunks.json
#   └─ FAST_DOCS/
#      └─ fastapi/
#         └─ fastapi/
#            └─ doc_chunks.json

collections = {}
seen_names = set()

_scan_directory_recursive(
    directory=Path("Chunked"),
    max_depth=5,
    chunked_dir=Path("Chunked"),
    collections=collections,
    seen_names=seen_names,
    current_depth=0
)

# After execution:
# collections = {
#   "Docling": Path("Chunked/Docling"),
#   "FAST_DOCS_fastapi_fastapi": Path("Chunked/FAST_DOCS/fastapi/fastapi")
# }
```

**Expected Log Output:**
```
INFO - Discovered collection 'Docling' with 1 chunk files
INFO - Discovered collection 'FAST_DOCS_fastapi_fastapi' with 1 chunk files
```

---

#### `discover_collections(chunked_dir: Path, max_depth: int = 5) -> dict[str, Path]`

**Purpose:** Main entry point for collection discovery (orchestrates recursive scan).

**Algorithm:**
```python
1. Validate chunked_dir exists and is a directory
2. Log start of discovery
3. Initialize collections dict and seen_names set
4. Call _scan_directory_recursive()
5. Log total collections found
6. Return collections dict
```

**Input:**
- `chunked_dir`: Root directory to scan
- `max_depth`: Maximum recursion depth (default 5)

**Output:**
- Dictionary mapping collection names to their directory paths

**Raises:**
- `ValueError`: If chunked_dir doesn't exist or isn't a directory

**Example:**
```python
collections = discover_collections(
    chunked_dir=Path("Chunked"),
    max_depth=5
)

# Returns:
# {
#   "Docling": Path("Chunked/Docling"),
#   "FAST_DOCS_fastapi": Path("Chunked/FAST_DOCS/fastapi"),
#   "Qdrant_qdrant_documentation_documentation": Path("..."),
#   ...
# }
```

**Expected Log Output:**
```
INFO - Scanning for collections in: Chunked
INFO - Max recursion depth: 5
INFO - Discovered collection 'Docling' with 46 chunk files
INFO - Discovered collection 'FAST_DOCS_fastapi' with 12 chunk files
INFO - Discovered collection 'Qdrant_qdrant_documentation_documentation' with 89 chunk files
...
INFO - Total collections discovered: 224
```

---

### 2. Processing Module

#### `_get_ensemble_mode_label(exclusive_mode: bool) -> str`

**Purpose:** Get human-readable label for ensemble mode.

**Algorithm:**
```python
return "EXCLUSIVE (model-at-a-time GPU lease)" if exclusive_mode else "PARALLEL"
```

**Input:**
- `exclusive_mode`: Boolean flag (always True in V6.1)

**Output:**
- String label for display: "EXCLUSIVE (model-at-a-time GPU lease)"

**Example:**
```python
_get_ensemble_mode_label(True)
# Returns: "EXCLUSIVE (model-at-a-time GPU lease)"

# Note: Parallel mode removed in V6.1
```

---

#### `_extract_telemetry(results: dict) -> tuple[list[str], list[dict], int]`

**Purpose:** Extract telemetry fields from embedder results with safe defaults.

**Algorithm:**
```python
1. Extract models_executed using RESULT_KEY_MODELS_EXECUTED (default [])
2. Extract lease_events using RESULT_KEY_LEASE_EVENTS (default [])
3. Extract total_embeddings using RESULT_KEY_TOTAL_EMBEDDINGS (default 0)
4. Return tuple of (models, events, count)
```

**Input:**
- `results`: Dictionary returned by embedder

**Output:**
- Tuple of (models_executed, lease_events, total_embeddings_count)

**Example:**
```python
results = {
    "models_executed": ["model1", "model2"],
    "lease_events": [
        {"event_type": "acquire", "model": "model1", "timestamp": "14:30:00"},
        {"event_type": "release", "model": "model1", "timestamp": "14:31:15"}
    ],
    "total_embeddings_generated": 1000
}

models, events, count = _extract_telemetry(results)

# Returns:
# models = ["model1", "model2"]
# events = [{"event_type": "acquire", ...}, ...]
# count = 1000

# Missing fields case:
models, events, count = _extract_telemetry({})
# Returns: ([], [], 0)
```

---

#### `_log_collection_completion(...) -> None`

**Purpose:** Log structured completion summary for a collection.

**Algorithm:**
```python
1. Log completion header with checkmark
2. Log models executed list
3. Log total embeddings count
4. If exclusive_mode and lease_events exist:
     log "GPU Lease Events:" header
     for each event:
       log event details (type, model, timestamp)
```

**Input:**
- `collection_name`: Name of completed collection
- `models_executed`: List of model names used
- `lease_events`: List of GPU lease event dicts
- `total_embeddings`: Total embeddings generated
- `exclusive_mode`: Whether exclusive mode was used

**Output:**
- None (logs to configured logger)

**Example:**
```python
_log_collection_completion(
    collection_name="Docling",
    models_executed=["model1", "model2"],
    lease_events=[
        {"event_type": "acquire", "model": "model1", "timestamp": "14:30:00"},
        {"event_type": "release", "model": "model1", "timestamp": "14:31:15"}
    ],
    total_embeddings=1000,
    exclusive_mode=True
)
```

**Expected Log Output:**
```
INFO - ✅ Completed collection: Docling
INFO -    Models executed: ['model1', 'model2']
INFO -    Total embeddings: 1000
INFO -    GPU Lease Events:
INFO -       - acquire: model1 @ 14:30:00
INFO -       - release: model1 @ 14:31:15
```

---

#### `process_collection(...) -> dict`

**Purpose:** Process a single collection through the embedding pipeline.

**Algorithm:**
```python
1. Get ensemble mode label and log header
2. Find chunk files in collection_dir
3. Validate chunk files exist (return {} if empty)
4. Log chunk file count
5. Call embedder.generate_embeddings_kaggle_optimized()
   → batch_runner.run() → batch_runner.run_exclusive_ensemble()
6. Validate results is a dict
7. Extract telemetry from results
8. Log completion summary
9. Return results dict
```

**Input:**
- `collection_name`: Name of collection
- `collection_dir`: Path to collection directory
- `embedder`: Initialized UltimateKaggleEmbedderV4 instance
- `args`: Parsed command-line arguments

**Output:**
- Dictionary with results and telemetry

**Raises:**
- `RuntimeError`: If embedding job fails or results invalid

**Example:**
```python
results = process_collection(
    collection_name="Docling",
    collection_dir=Path("Chunked/Docling"),
    embedder=embedder_instance,
    args=parsed_args
)

# Returns:
# {
#   "models_executed": ["model1", "model2", "model3"],
#   "lease_events": [{...}, {...}, ...],
#   "total_embeddings_generated": 1000,
#   "qdrant_collection": "Docling",
#   "processing_time": 75.3
# }
```

**Expected Log Output:**
```
INFO - ============================================================
INFO - Processing collection: Docling
INFO - Ensemble mode: EXCLUSIVE (model-at-a-time GPU lease)
INFO - ============================================================
INFO - Found 46 chunk files in Docling
INFO - ✅ Completed collection: Docling
INFO -    Models executed: ['model1', 'model2', 'model3']
INFO -    Total embeddings: 1000
INFO -    GPU Lease Events:
INFO -       - acquire: model1 @ 14:30:00
INFO -       - release: model1 @ 14:31:15
INFO -       - acquire: model2 @ 14:31:20
INFO -       - release: model2 @ 14:32:35
INFO -       - acquire: model3 @ 14:32:40
INFO -       - release: model3 @ 14:33:55
```

---

### 3. Orchestration Module

#### `_filter_collections(...) -> dict[str, Path]`

**Purpose:** Filter collections based on user request.

**Algorithm:**
```python
1. If requested is None:
     return all_collections (no filtering)
2. Convert requested to set
3. Convert all_collections.keys() to set
4. Check for missing collections
5. If any missing:
     raise ValueError with helpful message
6. Return filtered dict comprehension
```

**Input:**
- `all_collections`: Dict of all discovered collections
- `requested`: Optional list of requested collection names

**Output:**
- Filtered dictionary of collections

**Raises:**
- `ValueError`: If requested collections don't exist

**Example:**
```python
all_cols = {
    "Docling": Path("Chunked/Docling"),
    "FAST_DOCS": Path("Chunked/FAST_DOCS"),
    "Qdrant": Path("Chunked/Qdrant")
}

# Case 1: No filter requested
filtered = _filter_collections(all_cols, None)
# Returns: all_cols (unchanged)

# Case 2: Filter to subset
filtered = _filter_collections(all_cols, ["Docling", "Qdrant"])
# Returns: {"Docling": Path(...), "Qdrant": Path(...)}

# Case 3: Invalid request
try:
    filtered = _filter_collections(all_cols, ["NonExistent"])
except ValueError as e:
    print(e)
# Raises: ValueError with message showing available collections
```

---

#### `_initialize_embedder(...) -> UltimateKaggleEmbedderV4`

**Purpose:** Create and configure embedder with all necessary config objects.

**Algorithm:**
```python
1. Create EnsembleConfig with model_names, weights, normalization
2. Create KaggleGPUConfig with exclusive_ensemble_mode settings
3. Create KaggleExportConfig with Qdrant output settings
4. Try to instantiate UltimateKaggleEmbedderV4
5. If exception: log error and raise RuntimeError with context
6. Return embedder instance
```

**Input:**
- `ensemble_models`: List of model names/paths
- `exclusive_mode`: Boolean for exclusive GPU mode
- `ensemble_weights`: Optional list of weights (None for equal weights)

**Output:**
- Initialized UltimateKaggleEmbedderV4 instance

**Raises:**
- `RuntimeError`: If embedder initialization fails

**Example:**
```python
embedder = _initialize_embedder(
    ensemble_models=[
        "sentence-transformers/all-MiniLM-L6-v2",
        "BAAI/bge-small-en-v1.5"
    ],
    exclusive_mode=True,
    ensemble_weights=None
)

# Returns: UltimateKaggleEmbedderV4 instance ready to use
```

**Expected Log Output:**
```
# Success case: No direct logs (embedder logs internally)

# Error case:
ERROR - Failed to initialize embedder: CUDA out of memory
```

---

#### `_log_processing_summary(...) -> None`

**Purpose:** Log final summary of all collection processing.

**Algorithm:**
```python
1. Calculate total, succeeded, failed counts
2. Log header separator
3. Log "PROCESSING COMPLETE"
4. Log counts (total, succeeded, failed)
5. If any failed collections:
     log failed collections list with exception types
```

**Input:**
- `results`: Dict of successful collection results
- `failed_collections`: Dict of failed collection exceptions

**Output:**
- None (logs to configured logger)

**Example:**
```python
_log_processing_summary(
    results={
        "Docling": {...},
        "FAST_DOCS": {...}
    },
    failed_collections={
        "Qdrant": RuntimeError("Connection timeout")
    }
)
```

**Expected Log Output:**
```
INFO - 
INFO - ============================================================
INFO - PROCESSING COMPLETE
INFO - ============================================================
INFO - Total collections: 3
INFO - Successfully processed: 2
INFO - Failed: 1
INFO - 
ERROR - Failed collections:
ERROR -   - Qdrant: RuntimeError: Connection timeout
```

---

#### `_export_summary_json(...) -> None`

**Purpose:** Export processing summary to JSON file.

**Algorithm:**
```python
1. Build summary dict with:
     - timestamp (current datetime as ISO string)
     - environment (detect Kaggle or Local)
     - ensemble_models list
     - exclusive_ensemble_mode boolean
     - results dict
     - failed_collections dict (converted exceptions to strings)
2. Try to write JSON with indent=2
3. Log success with file path
4. If exception: log error
```

**Input:**
- `results`: Dict of collection results
- `output_file`: Path where JSON should be written
- `ensemble_models`: List of model names used
- `exclusive_mode`: Boolean ensemble mode

**Output:**
- None (writes JSON file)

**Side Effects:**
- Creates/overwrites JSON file at output_file path

**Example:**
```python
_export_summary_json(
    results={"Docling": {...}},
    output_file=Path("output/embedding_summary_v6.json"),
    ensemble_models=["model1", "model2"],
    exclusive_mode=True
)
```

**Expected JSON Output:**
```json
{
  "timestamp": "2025-10-22T14:35:22.123456",
  "environment": "Kaggle",
  "ensemble_models": [
    "sentence-transformers/all-MiniLM-L6-v2",
    "BAAI/bge-small-en-v1.5",
    "nomic-ai/nomic-embed-text-v1.5"
  ],
  "exclusive_ensemble_mode": true,
  "results": {
    "Docling": {
      "models_executed": ["model1", "model2", "model3"],
      "lease_events": [...],
      "total_embeddings_generated": 1000,
      "qdrant_collection": "Docling"
    }
  },
  "failed_collections": {}
}
```

**Expected Log Output:**
```
INFO - Summary exported to output/embedding_summary_v6.json
```

---

#### `main() -> None`

**Purpose:** Main orchestration function (entry point when script is executed).

**Algorithm:**
```python
1. Parse command-line arguments
2. Setup logging (file + stream handlers)
3. Discover all collections
4. Validate collections were found
5. Filter to requested collections
6. Initialize embedder
7. For each collection to process:
     try:
       process collection and store results
     except Exception:
       store in failed_collections and log error
8. Log processing summary
9. Export summary JSON
10. Log completion message
```

**Input:**
- None (reads from sys.argv via parse_arguments)

**Output:**
- None (side effects: logs, JSON file, Qdrant collections)

**Side Effects:**
- Configures logging
- Creates Qdrant collections
- Writes log file
- Writes JSON summary file

**Example:**
```python
# Invoked via: python scripts/embed_collections_v6.py --exclusive_ensemble
if __name__ == "__main__":
    main()
```

**Expected Complete Log Output:**
```
2025-10-22 14:30:00 - INFO - Scanning for collections in: Chunked
2025-10-22 14:30:00 - INFO - Max recursion depth: 5
2025-10-22 14:30:01 - INFO - Discovered collection 'Docling' with 46 chunk files
2025-10-22 14:30:01 - INFO - Discovered collection 'FAST_DOCS_fastapi' with 12 chunk files
2025-10-22 14:30:02 - INFO - Total collections discovered: 224
2025-10-22 14:30:02 - INFO - Initializing embedder...
2025-10-22 14:30:05 - INFO - ============================================================
2025-10-22 14:30:05 - INFO - Processing collection: Docling
2025-10-22 14:30:05 - INFO - Ensemble mode: EXCLUSIVE (model-at-a-time GPU lease)
2025-10-22 14:30:05 - INFO - ============================================================
2025-10-22 14:30:05 - INFO - Found 46 chunk files in Docling
2025-10-22 14:32:20 - INFO - ✅ Completed collection: Docling
2025-10-22 14:32:20 - INFO -    Models executed: ['model1', 'model2', 'model3']
2025-10-22 14:32:20 - INFO -    Total embeddings: 1000
2025-10-22 14:32:20 - INFO -    GPU Lease Events:
2025-10-22 14:32:20 - INFO -       - acquire: model1 @ 14:30:10
2025-10-22 14:32:20 - INFO -       - release: model1 @ 14:31:25
... (repeat for all collections) ...
2025-10-22 15:45:30 - INFO - 
2025-10-22 15:45:30 - INFO - ============================================================
2025-10-22 15:45:30 - INFO - PROCESSING COMPLETE
2025-10-22 15:45:30 - INFO - ============================================================
2025-10-22 15:45:30 - INFO - Total collections: 224
2025-10-22 15:45:30 - INFO - Successfully processed: 224
2025-10-22 15:45:30 - INFO - Failed: 0
2025-10-22 15:45:31 - INFO - Summary exported to output/embedding_summary_v6.json
2025-10-22 15:45:31 - INFO - Processing complete!
```

---

### 4. Argument Parsing

#### `parse_arguments() -> argparse.Namespace`

**Purpose:** Parse command-line arguments with environment-aware defaults.

**Algorithm:**
```python
1. Detect environment (check if "/kaggle" in current working directory)
2. Set defaults based on environment:
     Kaggle: chunked_dir="/kaggle/input/.../Chunked"
     Local: chunked_dir="./Chunked"
3. Create ArgumentParser with description and epilog
4. Add all argument definitions with types and defaults
5. Parse sys.argv and return Namespace
```

**Input:**
- None (reads sys.argv)

**Output:**
- `argparse.Namespace` with parsed arguments

**Arguments:**
- `--chunked_dir`: Path to chunked documents directory
- `--output_dir`: Path for output files
- `--collections`: Optional list of specific collections to process
- `--ensemble_models`: List of model names for ensemble
- `--ensemble_weights`: Optional list of weights for ensemble
- `--exclusive_ensemble`: Flag to enable exclusive GPU mode
- `--batch_size`: Batch size for embedding
- `--model_cache_dir`: Directory for model caching
- `--qdrant_host`: Qdrant server host
- `--qdrant_port`: Qdrant server port
- `--verbose`: Enable debug logging

**Example:**
```bash
# Minimal invocation (uses all defaults)
python scripts/embed_collections_v6.py

# Full specification
python scripts/embed_collections_v6.py \
  --chunked_dir /kaggle/input/mydata/Chunked \
  --output_dir /kaggle/working \
  --collections Docling FAST_DOCS \
  --exclusive_ensemble \
  --ensemble_models model1 model2 model3 \
  --batch_size 64 \
  --verbose
```

**Parsed Output:**
```python
Namespace(
    chunked_dir=Path('/kaggle/input/mydata/Chunked'),
    output_dir=Path('/kaggle/working'),
    collections=['Docling', 'FAST_DOCS'],
    ensemble_models=['model1', 'model2', 'model3'],
    ensemble_weights=None,
    exclusive_ensemble=True,
    batch_size=64,
    model_cache_dir=Path('/kaggle/working/hf_cache'),
    qdrant_host='localhost',
    qdrant_port=6333,
    verbose=True
)
```

---

## Output Specifications

### 1. Qdrant Collections

**Location:** Qdrant vector database (localhost:6333 or configured host)

**Structure per Collection:**
```
Collection Name: "Docling" (matches collection_name)
│
├─ Configuration:
│  ├─ Vector Size: 384 (for all-MiniLM-L6-v2 ensemble)
│  ├─ Distance Metric: Cosine
│  └─ On-Disk Storage: Enabled
│
└─ Points (embeddings):
   ├─ Point 1:
   │  ├─ id: UUID or sequential int
   │  ├─ vector: [0.123, -0.456, 0.789, ...] (384-dim)
   │  └─ payload: {
   │       "text": "Original chunk text content",
   │       "chunk_id": "doc1_chunk_0",
   │       "doc_id": "doc1",
   │       "metadata": {...}
   │     }
   │
   ├─ Point 2: ...
   └─ Point N: ...

Total Points: 1000 (example)
```

### 2. Log File

**Location:** `{output_dir}/embedding_v6.log`

**Format:** Standard Python logging format
```
{timestamp} - {level} - {message}
```

**Content Sections:**
1. **Initialization**
   - Environment detection
   - Collection discovery progress

2. **Per-Collection Processing**
   - Collection start header
   - Ensemble mode indication
   - Chunk file count
   - GPU lease events (exclusive mode only)
   - Completion summary

3. **Final Summary**
   - Total/success/failure counts
   - Failed collection details (if any)

**Size:** Varies (typically 10KB - 1MB depending on collection count)

### 3. JSON Summary File

**Location:** `{output_dir}/embedding_summary_v6.json`

**Schema:**
```json
{
  "timestamp": "ISO-8601 datetime string",
  "environment": "Kaggle" | "Local",
  "ensemble_models": ["model1", "model2", ...],
  "exclusive_ensemble_mode": true | false,
  "results": {
    "{collection_name}": {
      "models_executed": ["model1", "model2", ...],
      "lease_events": [
        {
          "event_type": "acquire" | "release",
          "model": "model_name",
          "timestamp": "ISO-8601 datetime string"
        }
      ],
      "total_embeddings_generated": integer,
      "qdrant_collection": "collection_name",
      "processing_time": float (seconds)
    }
  },
  "failed_collections": {
    "{collection_name}": "Exception message string"
  }
}
```

**Example:**
```json
{
  "timestamp": "2025-10-22T14:35:22.123456",
  "environment": "Kaggle",
  "ensemble_models": [
    "sentence-transformers/all-MiniLM-L6-v2",
    "BAAI/bge-small-en-v1.5",
    "nomic-ai/nomic-embed-text-v1.5"
  ],
  "exclusive_ensemble_mode": true,
  "results": {
    "Docling": {
      "models_executed": [
        "sentence-transformers/all-MiniLM-L6-v2",
        "BAAI/bge-small-en-v1.5",
        "nomic-ai/nomic-embed-text-v1.5"
      ],
      "lease_events": [
        {
          "event_type": "acquire",
          "model": "sentence-transformers/all-MiniLM-L6-v2",
          "timestamp": "2025-10-22T14:30:10.456789"
        },
        {
          "event_type": "release",
          "model": "sentence-transformers/all-MiniLM-L6-v2",
          "timestamp": "2025-10-22T14:31:25.123456"
        },
        {
          "event_type": "acquire",
          "model": "BAAI/bge-small-en-v1.5",
          "timestamp": "2025-10-22T14:31:30.789012"
        },
        {
          "event_type": "release",
          "model": "BAAI/bge-small-en-v1.5",
          "timestamp": "2025-10-22T14:32:45.345678"
        },
        {
          "event_type": "acquire",
          "model": "nomic-ai/nomic-embed-text-v1.5",
          "timestamp": "2025-10-22T14:32:50.901234"
        },
        {
          "event_type": "release",
          "model": "nomic-ai/nomic-embed-text-v1.5",
          "timestamp": "2025-10-22T14:34:05.567890"
        }
      ],
      "total_embeddings_generated": 1000,
      "qdrant_collection": "Docling",
      "processing_time": 235.4
    }
  },
  "failed_collections": {}
}
```

### 4. ZIP Archive Export (Optional)

**Location:** `{output_dir}/embeddings_{timestamp}.zip`  
**Enabled By:** `--create-zip` CLI flag  
**Compression:** Configurable via `--zip-compression` (deflated/stored)

**Purpose:** Package all embeddings and metadata into a single downloadable archive for distribution, backup, or transfer between environments.

**Contents:**
```
embeddings_2025-10-23_14-30-45.zip
├── MANIFEST.txt                    ← File listing with sizes
├── embedding_summary_v6.json       ← Processing summary
├── Docling/
│   ├── Docling_embeddings.npy     ← Dense embeddings (NumPy)
│   ├── Docling_metadata.json      ← Chunk metadata
│   ├── Docling_texts.json         ← Original chunk texts
│   ├── Docling_sparse.jsonl       ← Sparse vectors (if enabled)
│   ├── Docling_stats.json         ← Collection statistics
│   └── Docling_upload_script.py   ← Ready-to-use Qdrant upload script
├── pydantic/
│   └── ... (same structure)
└── ... (all other collections)
```

**MANIFEST.txt Format:**
```
EMBEDDING ARCHIVE MANIFEST
================================================================================
Generated: 2025-10-23T14:35:22.123456
Compression: deflated
================================================================================

FILES:

  Docling/Docling_embeddings.npy                                   12.34 MB
  Docling/Docling_metadata.json                                     2.56 MB
  Docling/Docling_texts.json                                        3.78 MB
  ... (all files listed)

================================================================================
SUMMARY:
  Total files: 1236
  Total size: 512.34 MB
================================================================================
```

**Archive Verification:**
- Automatically verified with `zipfile.testzip()` after creation
- File count validated
- Compression ratio logged
- Space savings reported

**Typical Workflow:**
1. **Generate embeddings** on Kaggle GPU or server
2. **Create ZIP** with `--create-zip` flag
3. **Download** single file instead of thousands of individual files
4. **Extract** locally and upload to local Qdrant instance
5. **Upload** using included per-collection scripts

**Size Estimates:**
- Uncompressed: ~500-600 MB (224 collections, 50K chunks)
- Compressed (deflated): ~250-300 MB (50-60% reduction)
- Stored (no compression): Same as uncompressed

**Use Cases:**
- **Kaggle → Local**: Generate on GPU, download, upload to local Qdrant
- **Collaboration**: Share complete embedding datasets
- **Backup**: Archive for long-term storage
- **Portability**: Move between cloud providers or environments

---

## Usage Examples

### Example 1: Local Development (All Collections - Exclusive Mode Only)

```bash
# Process all collections with exclusive mode (ONLY MODE)
python scripts/embed_collections_v6.py \
  --chunked_dir ./Chunked \
  --output_dir ./output \
  --verbose
```

**Expected Behavior:**
- Discovers all 224 collections
- Processes each with exclusive ensemble (one model at a time)
- Safer GPU memory usage, works on any hardware
- Creates 224 Qdrant collections
- Outputs log and JSON summary

**Estimated Time:** 1-2 hours (depending on hardware)

---

### Example 2: Kaggle Production (Exclusive Mode Only)

```bash
# Kaggle notebook cell (exclusive mode automatic)
!python scripts/embed_collections_v6.py \
  --chunked_dir /kaggle/input/yourdata/Chunked \
  --output_dir /kaggle/working
```

**Expected Behavior:**
- Discovers all collections in Kaggle input dataset
- Processes each with exclusive ensemble (one model at a time)
- GPU lease events logged for debugging
- Works within Kaggle T4x2 constraints
- Outputs saved to /kaggle/working

**Estimated Time:** 2-4 hours (GPU lease overhead + 224 collections)

---

### Example 3: Process Specific Collections

```bash
# Only process Docling and FAST_DOCS collections
python scripts/embed_collections_v6.py \
  --chunked_dir ./Chunked \
  --collections Docling FAST_DOCS_fastapi
```

**Expected Behavior:**
- Discovers all 224 collections
- Filters to only Docling and FAST_DOCS_fastapi
- Processes 2 collections in exclusive mode
- Much faster iteration for testing

**Estimated Time:** 5-10 minutes

---

### Example 4: ZIP Archive Export for Distribution

```bash
# Create downloadable ZIP archive of all embeddings
python scripts/embed_collections_v6.py \
  --chunked_dir ./Chunked \
  --output_dir ./output \
  --create-zip \
  --zip-compression deflated
```

**Expected Behavior:**
- Processes all collections with exclusive ensemble
- Exports each collection to subdirectory: `output/{collection_name}/`
- Creates ZIP archive: `output/embeddings_2025-10-23_14-30-45.zip`
- Includes MANIFEST.txt with file list and sizes
- Verifies archive integrity after creation
- Logs compression ratio and space saved

**Output Structure:**
```
output/
├── Docling/
│   ├── Docling_embeddings.npy
│   ├── Docling_metadata.json
│   ├── Docling_texts.json
│   ├── Docling_sparse.jsonl
│   ├── Docling_stats.json
│   └── Docling_upload_script.py
├── pydantic/
│   ├── pydantic_embeddings.npy
│   └── ... (same structure)
├── embedding_summary_v6.json
├── MANIFEST.txt
└── embeddings_2025-10-23_14-30-45.zip  ← All of the above archived
```

**Workflow:**
1. **Process & Export**: Run script with `--create-zip`
2. **Download**: Transfer ZIP file from server/Kaggle
3. **Extract**: Unzip on local machine
4. **Upload to Qdrant**: Use provided upload scripts

**Use Cases:**
- **Kaggle**: Generate embeddings on GPU, download ZIP to local Qdrant instance
- **Distribution**: Share complete embedding datasets with collaborators
- **Backup**: Archive embedding outputs for long-term storage
- **Portability**: Move embeddings between environments

**Estimated Time:** Same as processing + 1-5 minutes for ZIP creation

---

### Example 5: Custom Ensemble Weights

```bash
# Use weighted ensemble (emphasize first model)
python scripts/embed_collections_v6.py \
  --ensemble_models model1 model2 model3 \
  --ensemble_weights 0.5 0.3 0.2
```

**Expected Behavior:**
- model1 contributes 50% to final embedding
- model2 contributes 30%
- model3 contributes 20%
- Useful for prioritizing higher-quality models
- Works with exclusive mode (only mode in V6.1)

---

## Debugging Guide

### Common Issues

#### Issue 1: No Collections Discovered

**Symptom:**
```
INFO - Total collections discovered: 0
ERROR - No collections discovered.
```

**Diagnosis:**
- Check chunk file pattern matches (`*_chunks.json`)
- Verify directory structure
- Check max_depth is sufficient

**Fix:**
```bash
# Verify chunk files exist
ls -R Chunked/ | grep chunks.json

# Increase max depth if needed
python scripts/embed_collections_v6.py --chunked_dir ./Chunked  # Already uses max_depth=5
```

---

#### Issue 2: Requested Collections Not Found

**Symptom:**
```
ERROR - None of the requested collections were found.
ERROR - Requested: {'MyCollection'}
ERROR - Available: {'Docling', 'FAST_DOCS_fastapi', ...}
```

**Diagnosis:**
- Collection name mismatch (check for path-based names)
- Typo in collection name

**Fix:**
```bash
# List discovered collections first
python scripts/embed_collections_v6.py --verbose 2>&1 | grep "Discovered collection"

# Use exact names from discovery
python scripts/embed_collections_v6.py --collections Docling "FAST_DOCS_fastapi"
```

---

#### Issue 3: GPU Out of Memory

**Symptom:**
```
ERROR - Failed to initialize embedder: CUDA out of memory
```

**Diagnosis:**
- Batch size too large for available GPU memory
- Multiple models in ensemble may increase memory usage during model loading

**Fix:**
```bash
# Reduce batch size if encountering memory issues
python scripts/embed_collections_v6.py --batch_size 32

# Or reduce to even smaller batches
python scripts/embed_collections_v6.py --batch_size 16
```

**Note**: V6.1 uses exclusive mode only (model-at-a-time), which significantly reduces memory requirements compared to the old parallel mode.

---

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Discovery | O(n) | n = total files/dirs in tree |
| Filtering | O(m) | m = collection count |
| Processing | O(c × d × b) | c=collections, d=chunks, b=batch_ops |

### Space Complexity

| Component | Space | Notes |
|-----------|-------|-------|
| Collections Map | O(n) | n = collection count |
| Chunk Files List | O(d) | d = chunks per collection |
| Embeddings (in-memory) | O(d × e) | e = embedding dimension (384) |
| GPU Memory (exclusive) | O(p) | Single model at a time (only mode) |

### Scalability

**Tested Configurations:**
- ✅ 224 collections (current)
- ✅ Up to 5 nesting levels
- ✅ 3-model ensemble
- ✅ Collections with 1-200 chunks

**Limits:**
- Max depth: 5 (configurable via MAX_DISCOVERY_DEPTH)
- GPU memory: Constrained by Kaggle T4x2 (2×16GB)
- Qdrant: No practical limit (uses disk storage)

---

## Conclusion

The refactored `embed_collections_v6.py` provides a production-grade embedding pipeline with:

1. **Robust Discovery**: Finds collections at any nesting depth
2. **Exclusive GPU Mode**: Sequential model execution with GPU lease management (ONLY MODE) ✅
3. **Comprehensive Logging**: Full telemetry including GPU lease events
4. **Environment Aware**: Automatic Kaggle vs Local detection
5. **Well-Tested**: 41 unit tests covering all functionality
6. **Maintainable**: Clean separation of concerns with extracted modules
7. **Throughput Monitoring**: Dedicated module for performance tracking

### V6.1 Architecture Improvements (October 23, 2025)

**Code Simplification:**
- Removed 445 lines of parallel mode code from batch_runner.py (35% reduction)
- Extracted ThroughputMonitor to dedicated module (145 lines)
- Reduced core.py by 30 lines through better modularization
- Total codebase reduction: 475 lines

**Benefits:**
- Single execution path (exclusive mode only)
- Improved maintainability and testability
- Reduced GPU memory complexity
- Better VRAM management for all hardware
- Zero OOM risks from parallel mode

Ready for deployment on Kaggle and all environments with simplified architecture! 🚀
