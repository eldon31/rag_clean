loss = {
    "dataset1": CoSENTLoss(model),
    "dataset2": MultipleNegativesRankingLoss(model)
}
```

Sources: [sentence_transformers/trainer.py:291-310]()

## Multi-Dataset Training

The training system supports training on multiple datasets simultaneously using `DatasetDict`:

```mermaid
graph TB
    subgraph "Multi-Dataset Input"
        DD["DatasetDict"]
        DS1["Dataset 'nli'"]
        DS2["Dataset 'sts'"] 
        DS3["Dataset 'quora'"]
    end
    
    subgraph "Loss Mapping"
        LossDict["Loss Dictionary"]
        L1["nli: CoSENTLoss"]
        L2["sts: CosineSimilarityLoss"]
        L3["quora: MNRL"]
    end
    
    subgraph "Batch Sampling"
        BatchSampler["MultiDatasetBatchSampler"]
        RoundRobin["RoundRobinBatchSampler"]
        Proportional["ProportionalBatchSampler"]
    end
    
    subgraph "Training Process"
        DataCollator["add_dataset_name_column()"]
        ComputeLoss["compute_loss()"]
        LossSelect["Select loss by dataset_name"]
    end
    
    DD --> DS1
    DD --> DS2
    DD --> DS3
    
    LossDict --> L1
    LossDict --> L2  
    LossDict --> L3
    
    DS1 --> BatchSampler
    DS2 --> BatchSampler
    DS3 --> BatchSampler
    
    BatchSampler --> RoundRobin
    BatchSampler --> Proportional
    
    BatchSampler --> DataCollator
    DataCollator --> ComputeLoss
    LossDict --> LossSelect
    ComputeLoss --> LossSelect
```

**Multi-Dataset Training Architecture**

Sources: [sentence_transformers/trainer.py:295-310](), [sentence_transformers/trainer.py:416-422](), [sentence_transformers/trainer.py:785-800]()

## Router Support for Asymmetric Training

The training system integrates with the `Router` module to enable asymmetric architectures where different paths are used for queries vs documents:

### Router Configuration

```python