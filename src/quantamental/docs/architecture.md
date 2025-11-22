# Quantamental Model - Architecture Documentation

## Solution Architecture

### High-Level Overview

The Quantamental Model is a machine learning system for stock screening that predicts which S&P 500 stocks are likely to outperform the market in the next month. The system combines quantitative (technical) and fundamental analysis.

```
┌─────────────────┐
│  FMP API        │  Financial data source
│  (Market Data)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Collection │  Async fetching of OHLCV + Fundamentals
│  (Notebook)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Processing │  Feature engineering + cleaning
│ & Feature Eng   │  Technical indicators + fundamental metrics
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Model Training │  Random Forest Classifier
│   (W&B Track)   │  Logs metrics, plots, artifacts
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Model Registry  │  Weights & Biases Artifacts
│   (W&B)         │  Versioned models + scalers
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Prediction    │  Download model, predict next month
│   & Backtest    │  Rank stocks by probability
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GCS Storage    │  Store predictions (CSV/Parquet)
│  (Output)       │  gs://fin-data-bucket-115/model_output/
└─────────────────┘
```

### Data Flow

1. **Data Ingestion**: Async API calls to FMP fetch S&P 500 constituents, historical OHLCV data, and quarterly/annual fundamental metrics
2. **Preprocessing**: Compute technical indicators (RSI, MACD, EMA, volatility), merge with fundamentals using time-based joins
3. **Feature Engineering**: Create 30+ features including lagged technicals and forward-filled fundamentals
4. **Training**: Random Forest trains on 12-month rolling window, predicting 1-month forward outperformance vs S&P 500
5. **Inference**: Load model from W&B, predict on latest month, rank stocks, upload top predictions to GCS

### Component Interactions

```
[FMP API] ──(fetch)──> [Data Layer] ──(process)──> [Feature Store]
                                                           │
                                                           ▼
[W&B] <──(log)── [Training Pipeline] <──(train)── [Model Layer]
   │                                                       │
   │                                                       ▼
   └────────────(download)────────> [Inference Pipeline]
                                            │
                                            ▼
                                      [GCS Bucket]
```

## Technical Architecture

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Data Source | FMP API | Financial market data |
| Data Processing | Pandas, NumPy | Data manipulation |
| Feature Engineering | Scikit-learn, Custom | Technical & fundamental features |
| ML Framework | Scikit-learn | Random Forest classifier |
| Experiment Tracking | Weights & Biases | Model versioning, metrics, artifacts |
| Cloud Storage | Google Cloud Storage | Output storage |
| Orchestration | Python scripts | Pipeline execution |
| Containerization | Docker | Packaging for deployment |
| CI/CD | GitHub Actions | Automated testing & deployment |

### Key Design Patterns

#### 1. Configuration Management
- **Pattern**: Centralized YAML configuration
- **Implementation**: `config.yaml` + environment variable overrides
- **Benefit**: Easy parameter tuning without code changes

#### 2. Separation of Concerns
- **Data Collection**: Isolated in notebook (async API calls)
- **Feature Engineering**: Separate processing step
- **Training**: Focused on model training + W&B logging
- **Inference**: Clean prediction pipeline
- **Storage**: Dedicated GCS handler

#### 3. Experiment Tracking
- **Pattern**: Full W&B integration
- **Tracks**: Hyperparameters, metrics, plots, models, datasets
- **Benefit**: Reproducibility, model comparison, lineage

#### 4. Artifact Versioning
- **Pattern**: W&B Artifacts for models & data
- **Implementation**: Tag-based versioning (`:latest`, `:v1`, etc.)
- **Benefit**: Rollback capability, audit trail

### Data Architecture

#### Storage Strategy

```
Local Storage (Development):
./data/
├── ohlcv_raw.parquet              # Cached OHLCV data
├── fundamentals_combined.parquet  # Cached fundamental data
├── quantamental_cleaned.parquet   # Processed features
├── sp500_index.csv                # Benchmark data
├── model_rf.pkl                   # Trained model
└── scaler.pkl                     # Feature scaler

W&B Artifacts (Versioning):
quantamental-model:latest/
├── model_rf.pkl
├── scaler.pkl
└── metadata.json

GCS Bucket (Production Output):
gs://fin-data-bucket-115/
└── model_output/
    └── predictions/
        ├── stock_predictions_20241120.parquet
        ├── stock_predictions_20241120.csv
        └── latest_predictions.parquet
```

#### Data Versioning Strategy

See [data_versioning.md](data_versioning.md) for detailed strategy.

**Key Points**:
- W&B Artifacts for model + preprocessed data versioning
- Every training run logs dataset fingerprint
- Reproducible experiments via config + data version tracking

### Model Architecture

#### Random Forest Classifier

**Hyperparameters**:
```yaml
n_estimators: 400     # Number of trees
max_depth: 8          # Tree depth limit
class_weight: balanced  # Handle imbalanced classes
random_state: 42      # Reproducibility
```

**Input Features** (30 total):
- 8 Technical indicators (lagged 1 period to prevent leakage)
- 22 Fundamental metrics (forward-filled for quarterly updates)

**Output**:
- Binary classification: Outperform (1) vs Underperform (0) S&P 500
- Probability scores for ranking

**Label Definition**:
```
label = 1 if (stock_return_next_month > sp500_return_next_month) else 0
```

#### Feature Engineering Pipeline

```python
Technical Features (lagged):
- return_1m_lag1
- ema_12_lag1, ema_26_lag1
- macd_lag1, macd_signal_lag1, macd_hist_lag1
- RSI_14_lag1
- volatility_21d_lag1

Fundamental Features (forward-filled):
- Profitability: roe, roic, returnOnTangibleAssets
- Valuation: peRatio, earningsYield, freeCashFlowYield
- Leverage: debtToEquity, netDebtToEBITDA
- Liquidity: currentRatio, interestCoverage
- Quality: incomeQuality, intangiblesToTotalAssets
- (+ 13 more)
```

### Deployment Strategy

#### Current (MS4): Local Development
- Manual execution of training and inference scripts
- Local model storage + W&B cloud tracking
- GCS for output persistence

#### Future (MS5): Kubernetes Production
```
┌──────────────────────────────────────────┐
│          Kubernetes Cluster              │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  Data Collection Pod               │ │
│  │  (Scheduled CronJob - Weekly)      │ │
│  └────────────────────────────────────┘ │
│                 │                        │
│                 ▼                        │
│  ┌────────────────────────────────────┐ │
│  │  Training Pod                      │ │
│  │  (Triggered on new data)           │ │
│  └────────────────────────────────────┘ │
│                 │                        │
│                 ▼                        │
│  ┌────────────────────────────────────┐ │
│  │  Inference Pod                     │ │
│  │  (REST API - FastAPI)              │ │
│  └────────────────────────────────────┘ │
│                                          │
└──────────────────────────────────────────┘
         │              │
         ▼              ▼
      [W&B]         [GCS Bucket]
```

### Security Considerations

1. **API Keys**: Stored as environment variables, never committed
2. **GCS Credentials**: Service account JSON via `GOOGLE_APPLICATION_CREDENTIALS`
3. **W&B Authentication**: API key via `WANDB_API_KEY`
4. **Secrets Management**: GitHub Secrets for CI/CD

### Performance Considerations

1. **Async Data Fetching**: Concurrent API calls with `aiohttp` (configurable concurrency)
2. **Caching**: Local parquet files avoid redundant API calls
3. **Feature Scaling**: StandardScaler for normalized input
4. **Model Size**: Random Forest (400 trees) ~50MB, fast inference (<1s for 500 stocks)

### Monitoring & Observability

1. **W&B Dashboard**: Real-time training metrics, model comparison
2. **Logging**: Python logging to file + console (configurable levels)
3. **GCS**: Timestamped predictions for historical tracking
4. **Future**: Prometheus + Grafana for production monitoring (MS5)

### Scalability

**Current Limitations**:
- FMP API rate limits (250 calls/day on free tier)
- Single-machine training (minutes for 400 trees)
- Manual execution

**MS5 Enhancements**:
- Kubernetes horizontal pod autoscaling
- Distributed training (if needed)
- Scheduled automation (CronJobs)
- Load balancing for API endpoints

## Design Decisions

### Why Random Forest?
- **Interpretable**: Feature importance for explainability
- **Robust**: Handles missing data, no assumption of linearity
- **Fast**: Training in minutes, inference in milliseconds
- **Proven**: Strong baseline for tabular financial data

### Why W&B over MLflow?
- **Ease of use**: Quick setup, no server management
- **Collaboration**: Cloud-hosted, shareable dashboards
- **Artifact management**: Built-in model registry
- **Free tier**: Sufficient for academic projects

### Why GCS over local storage?
- **Durability**: Cloud persistence vs local machine failures
- **Accessibility**: Team can access predictions
- **Integration**: Ready for MS5 Kubernetes deployment
- **Scalability**: Handles large prediction outputs

### Why monthly predictions?
- **Fundamental data**: Quarterly earnings → monthly resolution appropriate
- **Stability**: Reduces noise vs daily/weekly predictions
- **Practical**: Aligns with typical portfolio rebalancing

## Future Improvements

1. **Ensemble Models**: Combine RF with XGBoost, LightGBM
2. **Deep Learning**: LSTM for time series, transformers for sentiment
3. **Real-time API**: FastAPI endpoint for on-demand predictions
4. **Backtesting**: Historical performance validation
5. **Risk Management**: Portfolio construction with position sizing
6. **Alternative Data**: News sentiment, social media, insider trading

---

**Document Version**: 1.0  
**Last Updated**: November 2024  
**Author**: Stock Busters Team
