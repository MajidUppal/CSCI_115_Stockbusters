# Data Versioning Strategy - Quantamental Model

## Overview

This document describes the data versioning approach for the Quantamental Model project, including the methodology, justification, and usage instructions.

## Chosen Methodology: W&B Artifacts

### What is W&B Artifacts?

Weights & Biases Artifacts is a dataset and model versioning system that provides:
- Snapshot-based versioning (not diff-based like DVC)
- Automatic content-based deduplication
- Cloud storage integration
- Lineage tracking (which data → which model → which predictions)
- Tag-based versioning (`:latest`, `:v1`, `:production`)

### Why W&B Artifacts?

We chose W&B Artifacts over alternatives like DVC for the following reasons:

#### 1. **Integration with Experiment Tracking**
- **Single Platform**: Both experiments and data in one place
- **Automatic Lineage**: Track which dataset version trained which model
- **Unified Dashboard**: View data, metrics, and models together

#### 2. **Project Characteristics Match**
Our project has:
- **Static training data**: Historical financial data doesn't change after collection
- **Monthly updates**: New data added monthly, not continuously
- **Small-medium size**: ~500 stocks × 36 months × 50 features = ~10MB compressed

This fits snapshot-based versioning better than diff-based (DVC).

#### 3. **Cloud-Native**
- No local Git-LFS setup required
- Direct GCS integration
- Team collaboration without local storage management

#### 4. **Ease of Use**
```python
# Versioning is just 3 lines:
artifact = wandb.Artifact('training-data', type='dataset')
artifact.add_file('data/quantamental_cleaned.parquet')
run.log_artifact(artifact)
```

vs. DVC which requires:
```bash
dvc init
dvc remote add -d storage gs://bucket
dvc add data/file.parquet
git add data/file.parquet.dvc
git commit -m "Add data"
dvc push
```

#### 5. **Model-Data Co-versioning**
Every model artifact automatically links to:
- Dataset version used for training
- Config/hyperparameters
- Evaluation metrics
- Code commit hash

## Comparison: W&B Artifacts vs DVC

| Feature | W&B Artifacts | DVC |
|---------|--------------|-----|
| **Versioning Type** | Snapshot-based | Diff-based (Git-like) |
| **Storage** | W&B Cloud + GCS | Any cloud (S3, GCS, Azure) |
| **Git Integration** | Optional (via run metadata) | Required (`.dvc` files in Git) |
| **Deduplication** | Automatic (content-hash) | Manual (user manages) |
| **Lineage Tracking** | Built-in (data→model→results) | Manual (via pipelines) |
| **Team Collaboration** | Cloud dashboard | Git + cloud storage |
| **Setup Complexity** | Minimal (API key) | Moderate (Git + remote config) |
| **Best For** | ML experiments, static datasets | Large datasets, CI/CD pipelines |

### When to Use DVC Instead

DVC would be preferable if:
- Dataset is very large (>100GB) and benefits from Git-like diffs
- Team already has DVC infrastructure
- Need integration with existing CI/CD pipelines
- Want storage provider flexibility
- Don't need experiment tracking

For our use case (small-medium data, active experimentation, academic project), W&B Artifacts is the better fit.

## Implementation

### Data Versioning Workflow

```
1. Data Collection (Notebook)
   ↓
   Raw data → Local cache (parquet)
   
2. Data Processing
   ↓
   Processed data → Local file
   
3. Model Training
   ↓
   Log to W&B Artifacts:
   - Dataset (processed features)
   - Model (trained RF)
   - Scaler (StandardScaler)
   
4. Tag & Version
   ↓
   Automatic versioning: v0, v1, v2...
   Manual tags: :latest, :production, :experiment-xyz
```

### Code Implementation

#### Logging Dataset Artifact

```python
# In model_train.py
import wandb

run = wandb.init(project="Quantamental-model")

# Create dataset artifact
data_artifact = wandb.Artifact(
    name='quantamental-training-data',
    type='dataset',
    description='Processed S&P 500 stock features with labels',
    metadata={
        'stocks': 500,
        'features': 30,
        'date_range': '2022-11-01 to 2025-11-01',
        'preprocessing': 'technical_lagged_1period_fundamentals_ffill'
    }
)

# Add file(s)
data_artifact.add_file('data/quantamental_cleaned.parquet')
data_artifact.add_file('data/sp500_index.csv')

# Log artifact
run.log_artifact(data_artifact)
```

#### Logging Model Artifact

```python
# Create model artifact
model_artifact = wandb.Artifact(
    name='quantamental-model',
    type='model',
    description='Random Forest model for stock screening',
    metadata={
        'algorithm': 'RandomForest',
        'n_estimators': 400,
        'max_depth': 8,
        'training_samples': 5000,
        'test_accuracy': 0.68
    }
)

# Add model files
model_artifact.add_file('data/model_rf.pkl')
model_artifact.add_file('data/scaler.pkl')

# Link to dataset used
data_artifact = run.use_artifact('quantamental-training-data:latest')
model_artifact.metadata['trained_on_dataset'] = data_artifact.name

# Log model
run.log_artifact(model_artifact)
```

#### Retrieving Versioned Artifacts

```python
# In backtest.py
import wandb

run = wandb.init(project="Quantamental-model", job_type="inference")

# Download latest model
model_artifact = run.use_artifact('quantamental-model:latest', type='model')
model_dir = model_artifact.download()

# Access files
model_path = f"{model_dir}/model_rf.pkl"
scaler_path = f"{model_dir}/scaler.pkl"

# Load model
with open(model_path, 'rb') as f:
    model = pickle.load(f)
```

### Version History Example

After 3 training runs, W&B shows:

```
quantamental-training-data
├── v0 (2024-11-01) - Initial dataset, 480 stocks
├── v1 (2024-11-08) - Added 20 new S&P 500 members
└── v2 (2024-11-15) - Updated with latest fundamentals  [:latest]

quantamental-model
├── v0 (2024-11-01) - Baseline, trained on data:v0, AUC=0.65
├── v1 (2024-11-08) - Tuned hyperparams, trained on data:v1, AUC=0.67
└── v2 (2024-11-15) - Production, trained on data:v2, AUC=0.70  [:latest, :production]
```

## Reproducibility Guarantees

Every W&B run captures:

| Component | How Versioned |
|-----------|---------------|
| **Code** | Git commit hash in run metadata |
| **Data** | W&B Artifact with content hash |
| **Model** | W&B Artifact linked to data artifact |
| **Config** | Logged as W&B config (hyperparameters) |
| **Environment** | `requirements.txt` + Python version in run |
| **Results** | Metrics, plots, predictions all logged |

### Reproducing a Past Run

```python
# Reproduce training run from 2024-11-15
run = wandb.init(project="Quantamental-model", id="abc123", resume="must")

# Download exact dataset used
data_artifact = run.use_artifact('quantamental-training-data:v2')
data_path = data_artifact.download()

# Use same config
config = run.config

# Train with same hyperparameters
model = RandomForestClassifier(**config)
# ... train ...
```

## Data Retrieval Instructions

### Setup W&B

```bash
# Install W&B
pip install wandb

# Login (one-time)
wandb login
# Paste API key from https://wandb.ai/authorize
```

### Download Latest Dataset

```bash
# CLI method
wandb artifact get stockbusters/Quantamental-model/quantamental-training-data:latest

# Python method
import wandb
run = wandb.init()
artifact = run.use_artifact('quantamental-training-data:latest')
artifact.download('./data')
```

### Download Specific Version

```python
# By version number
artifact = run.use_artifact('quantamental-training-data:v1')

# By tag
artifact = run.use_artifact('quantamental-training-data:production')

# By date (query API)
api = wandb.Api()
artifact = api.artifact('stockbusters/Quantamental-model/quantamental-training-data:v2')
```

## Data Lineage Tracking

### Viewing Lineage in W&B

Navigate to: `https://wandb.ai/<team>/Quantamental-model/artifacts`

**Lineage Graph**:
```
[quantamental-training-data:v2]
        ↓
    (used by)
        ↓
[quantamental-model:v2]
        ↓
    (generated)
        ↓
[predictions-2024-11-15]
```

### Querying Lineage Programmatically

```python
import wandb

api = wandb.Api()

# Get model artifact
model = api.artifact('stockbusters/Quantamental-model/quantamental-model:latest')

# Find source dataset
for artifact in model.logged_by().used_artifacts():
    if artifact.type == 'dataset':
        print(f"Trained on: {artifact.name}")
        print(f"  Version: {artifact.version}")
        print(f"  Created: {artifact.created_at}")
```

## Data Quality Checks

Before logging artifacts, we perform validation:

```python
def validate_dataset(df):
    """Validate dataset before versioning."""
    checks = {
        'no_missing_labels': df['label'].isna().sum() == 0,
        'features_complete': df[feature_names].isna().sum().sum() < len(df) * 0.05,
        'date_range_valid': (df['date'].max() - df['date'].min()).days > 365,
        'min_stocks': df['symbol'].nunique() >= 400,
        'balanced_labels': 0.3 < df['label'].mean() < 0.7
    }
    
    if not all(checks.values()):
        raise ValueError(f"Dataset validation failed: {checks}")
    
    return True
```

## Metadata Tracking

Each artifact includes rich metadata:

```python
metadata = {
    # Data characteristics
    'n_samples': len(df),
    'n_features': len(feature_names),
    'n_stocks': df['symbol'].nunique(),
    'date_range': f"{df['date'].min()} to {df['date'].max()}",
    
    # Data quality
    'missing_values_pct': df[feature_names].isna().sum().sum() / df.size * 100,
    'label_balance': df['label'].mean(),
    
    # Processing info
    'technical_lag': 1,
    'fundamental_ffill': True,
    'scaling': 'StandardScaler',
    
    # Source info
    'api_source': 'FMP',
    'collection_date': datetime.now().isoformat(),
    'git_commit': os.popen('git rev-parse HEAD').read().strip()
}
```

## Storage Costs

W&B Artifacts pricing (as of 2024):
- **Academic/Free**: 100GB storage, unlimited tracking
- **Team**: $50/user/month, 200GB + $0.10/GB
- **Enterprise**: Custom pricing

Our project (~10MB/month new data) stays well within free tier.

## Backup Strategy

While W&B provides cloud backup, we also:
1. **Local copies**: Keep processed data locally during development
2. **GCS backup**: Upload raw data to separate GCS bucket
3. **Git tracking**: Store data collection scripts in Git

## Alternatives Considered

### DVC (Data Version Control)
- **Pros**: Industry standard, Git-like, storage agnostic
- **Cons**: More setup, less ML-native, no built-in lineage
- **Verdict**: Too complex for project timeline

### MLflow
- **Pros**: Full MLOps platform, experiment tracking
- **Cons**: Requires server setup, heavier than W&B
- **Verdict**: Overkill for academic project

### Git LFS (Large File Storage)
- **Pros**: Native Git integration
- **Cons**: Not designed for datasets, 1GB limit on free tier
- **Verdict**: Insufficient for our needs

### Cloud Storage Only (GCS)
- **Pros**: Simple, direct storage
- **Cons**: No versioning, no lineage, manual tracking
- **Verdict**: Missing critical features

## Future Enhancements

1. **Automated Validation**: CI/CD pipeline validates data before logging
2. **Data Drift Detection**: Monitor feature distributions over time
3. **Multi-dataset Experiments**: Compare models trained on different data subsets
4. **Dataset Catalogs**: Searchable metadata for data discovery

---

**Document Version**: 1.0  
**Last Updated**: November 2024  
**Author**: Stock Busters Team  
**Related**: [architecture.md](architecture.md)
