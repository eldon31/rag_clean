router = Router(
    sub_modules={
        "query": [efficient_module],
        "document": [contextual_module, pooling_module]
    },
    default_route="document"
)
```

Key attributes:
- `sub_modules`: `nn.ModuleDict` mapping task types to `nn.Sequential` module chains
- `default_route`: Default task when `task` not specified in features
- `allow_empty_key`: Whether to allow no default route
- `forward_kwargs`: List of kwargs forwarded to modules (includes `"task"`)

Sources: [sentence_transformers/models/Router.py:22-418](), [sentence_transformers/models/Router.py:187-215](), [sentence_transformers/models/Router.py:217-245]()

## Module Composition Examples

### Dense Embedding Model (SentenceTransformer)

```mermaid
graph LR
    Text["Input Text"] --> Transformer["Transformer<br/>(bert-base-uncased)"]
    Transformer --> Pooling["Pooling<br/>(mean pooling)"]
    Pooling --> Normalize["Normalize<br/>(L2 normalization)"]
    Normalize --> Embedding["Dense Embedding<br/>(768-dim vector)"]
    
    subgraph "modules[0]"
        Transformer
    end
    subgraph "modules[1]"
        Pooling
    end
    subgraph "modules[2]"
        Normalize
    end
```

### Asymmetric Model with Router

#### Asymmetric SparseEncoder Architecture

```mermaid
graph TD
    EncodeQuery["model.encode_query()"] --> RouterQuery["Router(task='query')"]
    EncodeDoc["model.encode_document()"] --> RouterDoc["Router(task='document')"]
    
    RouterQuery --> QueryPath["sub_modules['query']"]
    RouterDoc --> DocPath["sub_modules['document']"]
    
    QueryPath --> StaticEmb["SparseStaticEmbedding<br/>Pre-computed static weights"]
    DocPath --> MLMTrans["MLMTransformer<br/>Contextual MLM head"]
    
    StaticEmb --> QueryEmb["Sparse Query Embedding<br/>(efficient)"]
    MLMTrans --> SpladePool["SpladePooling<br/>max + log1p_relu activation"]
    SpladePool --> DocEmb["Sparse Document Embedding<br/>(contextual)"]
    
    subgraph RouterModule["Router Module"]
        QueryPath
        DocPath
        StaticEmb
        MLMTrans
        SpladePool
    end
```

#### Router Training Requirements

```python
# Training args must specify router_mapping
args = SparseEncoderTrainingArguments(
    router_mapping={
        "question": "query",      # Dataset column -> router task
        "positive": "document", 
        "negative": "document"
    }
)

# Data collator uses mapping to set task in features
collator = SparseEncoderDataCollator(
    tokenize_fn=model.tokenize,
    router_mapping=args.router_mapping
)
```

Sources: [sentence_transformers/models/Router.py:104-156](), [sentence_transformers/sparse_encoder/trainer.py:180-186](), [sentence_transformers/sparse_encoder/data_collator.py:55-68]()

### Training Pipeline Integration

```mermaid
flowchart TD
    Dataset["Training Dataset"] --> Collator["SentenceTransformerDataCollator"]
    Collator --> RouterMap{router_mapping?}
    
    RouterMap -->|Yes| TaskRoute["Add task to features<br/>based on column mapping"]
    RouterMap -->|No| DirectProcess["Process normally"]
    
    TaskRoute --> Model["Model.forward()"]
    DirectProcess --> Model
    
    Model --> Features["Processed Features"]
    Features --> Loss["Loss Function<br/>(MultipleNegativesRankingLoss, etc.)"]
```

Sources: [sentence_transformers/trainer.py:198-204](), [sentence_transformers/data_collator.py:55-68]()

## Module Loading and Saving

### Module Configuration System

Each module uses a configuration system for persistence:

```mermaid
graph TD
    Module["Module Instance"] --> Config["get_config_dict()"]
    Config --> Keys["config_keys<br/>['param1', 'param2']"]
    Keys --> JSON["config.json<br/>{param1: value1, param2: value2}"]
    
    subgraph "Save Process"
        Config
        Keys
        JSON
    end
    
    LoadJSON["config.json"] --> LoadConfig["load_config()"]
    LoadConfig --> LoadModule["Module.load()"]
    LoadModule --> NewInstance["Module Instance"]
    
    subgraph "Load Process"
        LoadJSON
        LoadConfig
        LoadModule
        NewInstance
    end
```

Key configuration attributes:
- `config_keys`: List of attributes to save/load
- `config_file_name`: Name of config file (usually `"config.json"`)
- `save_in_root`: Whether to save in model root or subfolder

### Model Directory Structure

```mermaid
graph TD
    ModelDir["model_directory/"] --> ModulesJSON["modules.json<br/>(module metadata)"]
    ModelDir --> ConfigST["config_sentence_transformers.json<br/>(model-level config)"]
    
    ModelDir --> Module0["0_Transformer/<br/>(or root if save_in_root=True)"]
    ModelDir --> Module1["1_Pooling/"]
    ModelDir --> Module2["2_Normalize/"]
    
    Module0 --> TransConfig["sentence_bert_config.json"]
    Module0 --> ModelFiles["model.safetensors<br/>tokenizer files"]
    
    Module1 --> PoolConfig["config.json"]
    Module2 --> NormConfig["(empty - no config needed)"]
```

The `modules.json` file contains metadata about each module:

| Field | Description |
|-------|-------------|
| `idx` | Module index in pipeline |
| `name` | Module identifier |
| `path` | Directory path relative to model root |
| `type` | Full Python class path |

Sources: [docs/sentence_transformer/usage/custom_models.rst:43-101]()

## Training Integration

### Data Flow in Training

```mermaid
sequenceDiagram
    participant Dataset
    participant Collator as SentenceTransformerDataCollator
    participant Model as Model Pipeline
    participant Loss as Loss Function
    
    Dataset->>Collator: Raw text columns
    Note over Collator: Apply prompts, router_mapping
    Collator->>Model: Tokenized features + task info
    
    loop For each module
        Model->>Model: module.forward(features)
        Note over Model: Update features dict
    end
    
    Model->>Loss: Final features
    Loss->>Loss: Compute loss value
```

### Router Training Requirements

When using `Router` modules, additional training configuration is required:

```python