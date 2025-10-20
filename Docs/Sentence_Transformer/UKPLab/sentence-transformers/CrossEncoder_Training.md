This document covers the training system for CrossEncoder models in sentence-transformers. CrossEncoders are designed for reranking and classification tasks where two texts are jointly encoded to produce similarity scores or class predictions.

For information about training SentenceTransformer models (bi-encoders), see [3.1](#3.1). For SparseEncoder training, see [3.2](#3.2). For loss function details specific to CrossEncoders, see [3.6](#3.6).

## CrossEncoder Training Architecture

CrossEncoder training follows a similar pattern to other model types in sentence-transformers but with specific adaptations for joint text encoding and ranking/classification tasks.

**CrossEncoder Training System Overview**
```mermaid
graph TB
    subgraph "Core Components"
        CE[CrossEncoder]
        CETrainer[CrossEncoderTrainer]
        CEArgs[CrossEncoderTrainingArguments]
        CELosses[CrossEncoder Losses]
        CEEvals[CrossEncoder Evaluators]
    end
    
    subgraph "Data Processing"
        Dataset[datasets.Dataset]
        DataCollator[Data Collator]
        HardNegMining[Hard Negatives Mining]
    end
    
    subgraph "Loss Functions"
        BCE[BinaryCrossEntropyLoss]
        MNR[MultipleNegativesRankingLoss]
        Lambda[LambdaLoss]
        ListNet[ListNetLoss]
        CrossEntropy[CrossEntropyLoss]
    end
    
    subgraph "Training Infrastructure"
        HFTrainer[Transformers Trainer]
        ModelCard[Model Card Generation]
        HFHub[Hugging Face Hub]
    end
    
    CE --> CETrainer
    Dataset --> DataCollator
    CEArgs --> CETrainer
    CELosses --> CETrainer
    CEEvals --> CETrainer
    
    BCE --> CELosses
    MNR --> CELosses
    Lambda --> CELosses
    ListNet --> CELosses
    CrossEntropy --> CELosses
    
    CETrainer --> HFTrainer
    CETrainer --> ModelCard
    ModelCard --> HFHub
    
    HardNegMining --> Dataset
```

Sources: [docs/cross_encoder/training_overview.md:1-500](), [docs/cross_encoder/loss_overview.md:1-100]()

## Training Components

CrossEncoder training involves six main components that work together to fine-tune models for ranking and classification tasks.

**CrossEncoder Training Data Flow**
```mermaid
graph LR
    subgraph "Input Data"
        TextPairs["(text_A, text_B) pairs"]
        Triplets["(query, positive, negative)"]
        Rankings["(query, [doc1, doc2, ...])"]
        Labels[Class Labels / Scores]
    end
    
    subgraph "Data Processing"
        DataCollator["Data Collator"]
        Tokenization[Tokenization]
        BatchFormat[Batch Formatting]
    end
    
    subgraph "Model & Loss"
        CrossEncoder[CrossEncoder Model]
        LossFunction[Loss Function]
        ForwardPass[Forward Pass]
    end
    
    subgraph "Training Loop"
        Optimizer[Optimizer]
        BackwardPass[Backward Pass]
        WeightUpdate[Weight Update]
    end
    
    subgraph "Evaluation"
        Evaluator[CrossEncoder Evaluator]
        Metrics[Metrics Calculation]
    end
    
    TextPairs --> DataCollator
    Triplets --> DataCollator
    Rankings --> DataCollator
    Labels --> DataCollator
    
    DataCollator --> Tokenization
    Tokenization --> BatchFormat
    
    BatchFormat --> CrossEncoder
    CrossEncoder --> ForwardPass
    ForwardPass --> LossFunction
    
    LossFunction --> BackwardPass
    BackwardPass --> Optimizer
    Optimizer --> WeightUpdate
    
    CrossEncoder --> Evaluator
    Evaluator --> Metrics
```

Sources: [docs/cross_encoder/training_overview.md:170-190](), [sentence_transformers/data_collator.py:35-120]()

### Model Initialization

CrossEncoder models are initialized by loading a pretrained transformers model with a sequence classification head. If the model doesn't have such a head, it's added automatically.

```python
from sentence_transformers import CrossEncoder