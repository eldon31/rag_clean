all_modules = [module.__class__ for module in model.modules()]
if Router in all_modules or Asym in all_modules:
    model_type += ["Asymmetric"]
if SparseStaticEmbedding in all_modules:
    model_type += ["Inference-free"]
```

Sources: [sentence_transformers/sparse_encoder/model_card.py:87-111]()

## Integration with Training

### Trainer Integration

Model card callbacks are automatically added during trainer initialization:

**Callback Registration**:
The `SentenceTransformerModelCardCallback` is automatically integrated during trainer initialization and responds to training lifecycle events.

**Hyperparameter Filtering** ([sentence_transformers/model_card.py:97-129]()):
The system tracks only meaningful hyperparameters, filtering out logging and infrastructure settings like `output_dir`, `logging_dir`, `eval_steps`, etc.

### Carbon Emissions Tracking

Integration with CodeCarbon for environmental impact measurement:

**Automatic Detection** ([sentence_transformers/model_card.py:63-68]()):
```python
callbacks = [callback for callback in trainer.callback_handler.callbacks 
            if isinstance(callback, CodeCarbonCallback)]
if callbacks:
    model.model_card_data.code_carbon_callback = callbacks[0]
```

Sources: [sentence_transformers/trainer.py:315-333](), [sentence_transformers/model_card.py:47-192]()

## Model Card Generation Workflow

### Version and Citation Management

The system automatically manages framework versions and academic citations:

**Version Tracking** ([sentence_transformers/model_card.py:217-236]()):
- Python, sentence-transformers, transformers, PyTorch versions
- Optional accelerate, datasets, tokenizers versions

**Citation Generation** ([sentence_transformers/model_card.py:411-440]()):
- Loss function citations from `loss.citation` attributes
- Automatic deduplication of identical citations
- BibTeX formatting for academic references

### Final Model Card Assembly

Model cards are generated through the `generate_model_card()` function which:

1. Compiles all tracked metadata into template variables
2. Renders the Jinja2 template with collected data
3. Generates usage code snippets based on model type
4. Creates evaluation tables from stored metrics
5. Produces the final README.md file

Sources: [sentence_transformers/model_card.py:217-263](), [sentence_transformers/model_card.py:411-441]()