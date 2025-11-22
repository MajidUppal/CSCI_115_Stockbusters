# 📦 GCS Output Files - Complete Reference

## Overview

When you run the Quantamental pipeline, it uploads **7 files** to your GCS bucket at:
```
gs://fin-data-bucket-115/model_output/
```

## 🤖 Agent-Required Files (3 files)

These are the **exact files** your agents need, matching your notebook output:

### 1. `combined_quantamental_hybrid_with_factors_and_backtest.csv`
**Purpose**: Main output file with predictions, factors, and backtest results

**Columns**:
- `symbol`: Stock ticker
- `date`: Prediction date
- `close`: Current close price
- `pred_prob`: Predicted probability of outperforming S&P 500
- `pred_rank`: Ranking by probability (1 = best)
- `hybrid_score`: Combined score from multiple factors
- `signal`: Binary signal (1 = buy, 0 = hold/sell)
- `position`: Position indicator
- `backtest_return`: Backtest return (if available)
- Plus all technical and fundamental features

**Location**: `gs://fin-data-bucket-115/model_output/combined_quantamental_hybrid_with_factors_and_backtest.csv`

**Usage by Agents**: Primary data source for stock recommendations

---

### 2. `company_profiles.csv`
**Purpose**: Company metadata (sector, industry, market cap, etc.)

**Columns**:
- `symbol`: Stock ticker
- `companyName`: Full company name
- `sector`: Business sector (e.g., Technology, Healthcare)
- `industry`: Specific industry
- `marketCap`: Market capitalization
- `country`: Company headquarters country
- `website`: Company website
- `description`: Business description
- `ceo`: CEO name
- `exchange`: Stock exchange

**Location**: `gs://fin-data-bucket-115/model_output/company_profiles.csv`

**Usage by Agents**: Contextual information for recommendations (sector allocation, company details)

---

### 3. `all_equity_curves.csv`
**Purpose**: Historical equity curves for all stocks

**Columns**:
- `symbol`: Stock ticker
- `date`: Date
- `equity_value`: Cumulative equity value (starts at $100)
- `return`: Period return

**Location**: `gs://fin-data-bucket-115/model_output/all_equity_curves.csv`

**Usage by Agents**: Performance visualization, backtesting validation

---

## 📊 Additional Pipeline Files (4 files)

These files are also uploaded for tracking and analysis:

### 4. `predictions_YYYYMM_TIMESTAMP.csv`
**Purpose**: Clean predictions output (main ranked list)

**Columns**: Same as combined file but more focused on core prediction columns

**Example**: `predictions_202511_20251120_143022.csv`

---

### 5. `predictions_YYYYMM_TIMESTAMP.parquet`
**Purpose**: Same as CSV but in Parquet format (more efficient)

**Example**: `predictions_202511_20251120_143022.parquet`

---

### 6. `summary_YYYYMM_TIMESTAMP.json`
**Purpose**: Summary statistics and metadata

**Contents**:
```json
{
  "timestamp": "2025-11-20T14:30:22",
  "prediction_month": "2025-11",
  "total_stocks": 485,
  "top_n": 10,
  "top_stocks": ["AAPL", "MSFT", "NVDA", ...],
  "top_probs": [0.782, 0.765, 0.754, ...],
  "mean_prob": 0.512,
  "std_prob": 0.123,
  "min_prob": 0.234,
  "max_prob": 0.823
}
```

---

## 📂 Complete GCS Structure

```
gs://fin-data-bucket-115/
└── model_output/
    ├── combined_quantamental_hybrid_with_factors_and_backtest.csv  ✅ AGENT FILE
    ├── company_profiles.csv                                         ✅ AGENT FILE
    ├── all_equity_curves.csv                                        ✅ AGENT FILE
    ├── predictions_202511_20251120_143022.csv                      📊 Pipeline output
    ├── predictions_202511_20251120_143022.parquet                  📊 Pipeline output
    └── summary_202511_20251120_143022.json                         📊 Pipeline output
```

## 🔄 File Update Frequency

- **Weekly**: All files are regenerated weekly (or on-demand)
- **Naming**: Agent files have **fixed names** (overwritten each run)
- **Timestamped**: Pipeline files have timestamps (preserved for history)

## 📥 How to Access Files

### Using gsutil:
```bash
# List all files
gsutil ls gs://fin-data-bucket-115/model_output/

# Download agent files
gsutil cp gs://fin-data-bucket-115/model_output/combined_quantamental_hybrid_with_factors_and_backtest.csv .
gsutil cp gs://fin-data-bucket-115/model_output/company_profiles.csv .
gsutil cp gs://fin-data-bucket-115/model_output/all_equity_curves.csv .
```

### Using Python:
```python
from google.cloud import storage
import pandas as pd
from io import BytesIO

# Initialize client
client = storage.Client()
bucket = client.bucket('fin-data-bucket-115')

# Download agent file
blob = bucket.blob('model_output/combined_quantamental_hybrid_with_factors_and_backtest.csv')
content = blob.download_as_bytes()
df = pd.read_csv(BytesIO(content))

print(f"Loaded {len(df)} predictions")
```

## 🤖 Agent Integration Guide

### Step 1: Configure Agent to Read from GCS

```python
GCS_BUCKET = "fin-data-bucket-115"
GCS_PREFIX = "model_output"

# File paths (fixed names)
COMBINED_FILE = f"{GCS_PREFIX}/combined_quantamental_hybrid_with_factors_and_backtest.csv"
PROFILES_FILE = f"{GCS_PREFIX}/company_profiles.csv"
EQUITY_FILE = f"{GCS_PREFIX}/all_equity_curves.csv"
```

### Step 2: Load Data in Agent

```python
from google.cloud import storage
import pandas as pd

def load_agent_data():
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)
    
    # Load combined predictions
    blob = bucket.blob(COMBINED_FILE)
    df_predictions = pd.read_csv(blob.download_as_string())
    
    # Load company profiles
    blob = bucket.blob(PROFILES_FILE)
    df_profiles = pd.read_csv(blob.download_as_string())
    
    # Load equity curves
    blob = bucket.blob(EQUITY_FILE)
    df_equity = pd.read_csv(blob.download_as_string())
    
    return df_predictions, df_profiles, df_equity
```

### Step 3: Use in Agent Logic

```python
# Get top recommendations
df_pred, df_prof, df_eq = load_agent_data()

top_10 = df_pred.nlargest(10, 'pred_prob')

for _, stock in top_10.iterrows():
    symbol = stock['symbol']
    prob = stock['pred_prob']
    
    # Get company info
    company = df_prof[df_prof['symbol'] == symbol].iloc[0]
    sector = company['sector']
    
    # Get equity curve
    equity = df_eq[df_eq['symbol'] == symbol]
    
    # Use in agent decision...
    print(f"{symbol} ({sector}): {prob:.2%} confidence")
```

## ✅ Verification Checklist

After running pipeline, verify these files exist:

```bash
# Check agent files (fixed names)
gsutil ls gs://fin-data-bucket-115/model_output/combined_quantamental_hybrid_with_factors_and_backtest.csv
gsutil ls gs://fin-data-bucket-115/model_output/company_profiles.csv
gsutil ls gs://fin-data-bucket-115/model_output/all_equity_curves.csv

# Should show: 3 files found

# Check file sizes (should be non-zero)
gsutil du -sh gs://fin-data-bucket-115/model_output/

# Download and verify
gsutil cp gs://fin-data-bucket-115/model_output/combined_quantamental_hybrid_with_factors_and_backtest.csv test.csv
wc -l test.csv  # Should show ~485+ lines (one per stock)
```

## 🔍 Data Quality Checks

### For combined file:
```python
df = pd.read_csv('combined_quantamental_hybrid_with_factors_and_backtest.csv')

# Check
assert len(df) > 400, "Should have ~485 stocks"
assert 'pred_prob' in df.columns, "Missing predictions"
assert df['pred_prob'].between(0, 1).all(), "Invalid probabilities"
assert 'signal' in df.columns, "Missing signals"
print("✅ Combined file OK")
```

### For company profiles:
```python
df_prof = pd.read_csv('company_profiles.csv')

# Check
assert len(df_prof) > 400, "Should have ~485 companies"
assert 'sector' in df_prof.columns, "Missing sector info"
assert 'symbol' in df_prof.columns, "Missing symbols"
print("✅ Company profiles OK")
```

### For equity curves:
```python
df_eq = pd.read_csv('all_equity_curves.csv')

# Check
assert len(df_eq) > 10000, "Should have multiple months per stock"
assert 'equity_value' in df_eq.columns, "Missing equity values"
assert 'symbol' in df_eq.columns, "Missing symbols"
print("✅ Equity curves OK")
```

## 📌 Important Notes

1. **Fixed Filenames**: The 3 agent files always have the **same names** (no timestamps)
   - This makes it easy for agents to reference
   - Each run overwrites previous version

2. **Timestamped Files**: Pipeline outputs include timestamps
   - Useful for historical tracking
   - Can compare different runs

3. **Data Freshness**: 
   - Files updated weekly (or on-demand)
   - Check `generated_at` timestamp in data
   - Or check GCS file modification time

4. **Backup Strategy**:
   - Keep timestamped versions for audit trail
   - Agent always reads latest (fixed name files)

## 🎯 Summary

**For Agents**: Use these 3 files with **fixed names**:
1. ✅ `combined_quantamental_hybrid_with_factors_and_backtest.csv`
2. ✅ `company_profiles.csv`
3. ✅ `all_equity_curves.csv`

**For Tracking**: Use timestamped files:
- `predictions_*.csv`
- `predictions_*.parquet`
- `summary_*.json`

All files are in: `gs://fin-data-bucket-115/model_output/`

---

**Status**: ✅ All 3 agent-required files are now created and uploaded by the pipeline!
