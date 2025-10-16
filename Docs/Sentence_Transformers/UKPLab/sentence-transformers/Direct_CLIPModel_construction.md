from sentence_transformers.models import CLIPModel
clip_model = CLIPModel(
    model_name='openai/clip-vit-base-patch32',
    processor_name='openai/clip-vit-base-patch32'
)
```

The `CLIPModel.load()` class method handles model restoration from disk, ensuring both the `transformers.CLIPModel` and `transformers.CLIPProcessor` components are properly loaded.

Sources: [sentence_transformers/models/CLIPModel.py:18-25](), [sentence_transformers/models/CLIPModel.py:102-121]()

## Serialization and Persistence

The `CLIPModel` implements custom save/load methods to properly handle both the model and processor components:

```mermaid
graph LR
    subgraph Save["save() Method"]
        SAVEMODEL["model.save_pretrained()"]
        SAVEPROC["processor.save_pretrained()"]
    end
    
    subgraph Load["load() Method"] 
        LOADPATH["load_dir_path()"]
        CONSTRUCT["CLIPModel(local_path)"]
    end
    
    Save --> DISK["Disk Storage"]
    DISK --> Load
```

This ensures that both the vision and text processing components are preserved during model serialization.

Sources: [sentence_transformers/models/CLIPModel.py:98-121]()