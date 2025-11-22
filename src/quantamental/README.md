# Quantamental Model - Stock Screening ML Pipeline

A production-ready machine learning pipeline for stock screening using Random Forest Classification with quantamental (quantitative + fundamental) features. The model predicts which stocks are likely to outperform the S&P 500 in the next month.

##  Project Overview

This project combines:
- **Technical Analysis**: Price momentum, moving averages, RSI, volatility
- **Fundamental Analysis**: Financial ratios, valuation metrics, profitability indicators
- **Machine Learning**: Random Forest classifier with class balancing
- **MLOps**: W&B for experiment tracking, GCS for artifact storage

##  Architecture

```
Data Collection (FMP API)
    ↓
Feature Engineering (Technical + Fundamental)
    ↓
Model Training (Random Forest + W&B)
    ↓
Prediction (Next Month Outperformers)
    ↓
Backtest & Upload (GCS Bucket)
```

##  Project Structure

```
src/quantamental/
├── config.yaml              # Central configuration
├── utils.py                 # GCS handler, config loader
├── data_collect.py          # Fetch data from FMP API
├── data_process.py          # Feature engineering & cleaning
├── model_train.py           # Train model with W&B
├── model_predict.py         # Generate predictions
├── backtest.py              # Rank & upload to GCS
├── main.py                  # Pipeline orchestration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

##  Quick Start

### Prerequisites

1. **Python 3.9+**
2. **API Keys:**
   - Financial Modeling Prep (FMP) API key
   - Weights & Biases account
   - Google Cloud Platform account with GCS bucket

### Installation

```bash
# Clone repository
cd src/quantamental

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional - can also use config.yaml)
export FMP_API_KEY="your_fmp_api_key"
export WANDB_API_KEY="your_wandb_api_key"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/gcs-credentials.json"
```

### Configuration

Edit `config.yaml` to customize:
- API credentials
- GCS bucket name and output folder
- Model hyperparameters
- Feature selection
- W&B project name

```yaml
# Example config.yaml
api:
  fmp_api_key: "YOUR_API_KEY"

gcs:
  bucket_name: "fin-data-bucket-115"
  output_folder: "model_output"

wandb:
  project: "Quantamental-model"

model:
  hyperparameters:
    n_estimators: 400
    max_depth: 8
```

##  Usage

### Run Full Pipeline

```bash
# Run everything end-to-end
python main.py --step all

# Force refresh data from API (ignore cache)
python main.py --step all --force-refresh

# Skip training if model already exists in W&B
python main.py --step all --skip-training
```

### Run Individual Steps

```bash
# Step 1: Collect data
python main.py --step collect

# Step 2: Process data
python main.py --step process

# Step 3: Train model
python main.py --step train

# Step 4: Generate predictions
python main.py --step predict

# Step 5: Backtest & upload
python main.py --step backtest
```

### Run Modules Directly

```bash
# Data collection
python data_collect.py

# Data processing
python data_process.py

# Model training with W&B
python model_train.py

# Prediction
python model_predict.py

# Backtest & GCS upload
python backtest.py
```

##  Model Details

### Features (30+ total)

**Technical Indicators (8):**
- 1-month return
- EMA (12, 26)
- MACD, MACD Signal, MACD Histogram
- RSI (14-day)
- 21-day volatility

**Fundamental Metrics (22):**
- Valuation: P/E, P/B, P/S, EV/EBITDA
- Profitability: ROE, ROIC, Return on Tangible Assets
- Financial Health: Debt-to-Equity, Current Ratio, Interest Coverage
- Cash Flow: FCF Yield, Operating Cash Flow per Share
- And more...

### Model Architecture

- **Algorithm**: Random Forest Classifier
- **Hyperparameters**:
  - n_estimators: 400
  - max_depth: 8
  - class_weight: balanced
- **Training Window**: 12 months rolling
- **Prediction Horizon**: 1 month ahead
- **Target**: Binary classification (outperform S&P 500 or not)

### Performance Metrics

The model is evaluated using:
- Accuracy
- Precision
- Recall
- F1 Score
- ROC AUC
- Confusion Matrix
- Feature Importance

All metrics are logged to W&B for tracking.

##  Outputs

### GCS Bucket Structure

```
gs://fin-data-bucket-115/model_output/
├── predictions_202511_20251120_143022.csv
├── predictions_202511_20251120_143022.parquet
└── summary_202511_20251120_143022.json
```

### Prediction Output Format

```csv
symbol,date,close,pred_prob,pred_rank,generated_at,model_version
AAPL,2025-11-30,185.50,0.7823,1,2025-11-20T14:30:22,quantamental-v1
MSFT,2025-11-30,420.30,0.7654,2,2025-11-20T14:30:22,quantamental-v1
...
```

### W&B Logging

Each run logs:
- Model hyperparameters
- Training/validation metrics
- Confusion matrix
- Feature importance plots
- Prediction probability distributions
- Model artifacts (for versioning)

##  Development

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/quantamental --cov-report=term-missing
```

### Code Quality

```bash
# Linting
flake8 src/quantamental/

# Formatting
black src/quantamental/
```

##  Troubleshooting

### Issue: W&B Authentication Error
**Solution**: Login to W&B
```bash
wandb login
```

### Issue: GCS Permission Denied
**Solution**: Ensure service account has Storage Object Admin role
```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:SERVICE_ACCOUNT_EMAIL" \
    --role="roles/storage.objectAdmin"
```

### Issue: FMP API Rate Limit
**Solution**: Reduce concurrency in config.yaml
```yaml
api:
  concurrency: 4  # Reduce from 8
```

##  Data Sources

- **Stock Data**: Financial Modeling Prep (FMP) API
- **Benchmark**: S&P 500 Index (^GSPC)
- **Universe**: S&P 500 constituents
- **Frequency**: Daily data, monthly predictions

##  Scheduled Runs

For weekly production runs, use cron:

```bash
# Add to crontab (runs every Monday at 9 AM)
0 9 * * 1 cd /path/to/src/quantamental && python main.py --step all --skip-training
```

##  Notes

- Model trains on 12 months of historical data
- Predictions are for the next month
- Features use lagged values to prevent lookahead bias
- Fundamentals are forward-filled (quarterly updates)
- Technical indicators are computed daily

##  Contributing

For MS4 submission:
1. Ensure all tests pass
2. Check code coverage >50%
3. Update documentation
4. Take screenshots of passing CI
5. Submit commit hash on Canvas


##  Team

Team Name: Stock Buster  
Members: Sirisom Pranivong
 Harvard CSCI-E 115 Course Project
---

**Last Updated**: November 2025  
**Version**: 1.0.0
