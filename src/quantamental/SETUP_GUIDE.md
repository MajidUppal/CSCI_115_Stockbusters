# 🚀 Quick Setup Guide - Quantamental Model

## ✅ Pre-deployment Checklist

### 1. Environment Setup (5 minutes)

```bash
# Navigate to your project directory
cd src/quantamental

# Install dependencies
pip install -r requirements.txt

# Verify installations
python -c "import pandas, numpy, sklearn, wandb, google.cloud.storage; print('✅ All packages installed')"
```

### 2. API Keys Configuration (5 minutes)

**Option A: Environment Variables (Recommended for production)**
```bash
export FMP_API_KEY="VXTY4Jz8jYbQ9R4PjjkmqJ8VLROXlC3Z"
export WANDB_API_KEY="35a05083157054c9f1d557c446fe9ebf9d2c3fda"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/gcs-key.json"
```

**Option B: Edit config.yaml directly**
```yaml
api:
  fmp_api_key: "VXTY4Jz8jYbQ9R4PjjkmqJ8VLROXlC3Z"
```

### 3. W&B Setup (2 minutes)

```bash
# Login to W&B
wandb login

# Verify W&B connection
python -c "import wandb; wandb.init(project='test'); print('✅ W&B connected')"
```

### 4. GCS Setup (10 minutes)

**Create Service Account:**
1. Go to GCP Console → IAM & Admin → Service Accounts
2. Create service account with "Storage Object Admin" role
3. Download JSON key
4. Set environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="../../secrets/stock-busters-service-account.json"
```

**Verify GCS Access:**
```bash
python -c "from google.cloud import storage; client = storage.Client(); print('✅ GCS connected')"
```

### 5. Test Configuration (2 minutes)

```bash
# Test config loading
python -c "from utils import load_config; config = load_config(); print('✅ Config loaded')"

# Verify all paths
python utils.py
```

## 🎯 Quick Test Run (End-to-End)

### Option 1: Test with Cached Data (Fastest - 5 minutes)

If you already have data in `./data/` folder:

```bash
# Just test training and prediction
python main.py --step train
python main.py --step predict
python main.py --step backtest
```

### Option 2: Full Pipeline from Scratch (30-45 minutes)

```bash
# Run complete pipeline
python main.py --step all

# This will:
# 1. Fetch S&P 500 data from FMP (10 min)
# 2. Process features (5 min)
# 3. Train model with W&B logging (5 min)
# 4. Generate predictions (2 min)
# 5. Upload to GCS (1 min)
```

### Option 3: Weekly Production Run (10 minutes)

If model is already trained in W&B:

```bash
# Skip training, use existing model
python main.py --step all --skip-training
```

## 📊 Verify Outputs

### Check Local Files

```bash
ls -lh data/
# Should see:
# - quantamental_monthly.parquet
# - predictions_*.csv
# - models/*/model.pkl
```

### Check W&B Dashboard

1. Go to https://wandb.ai
2. Navigate to "Quantamental-model" project
3. Verify you see:
   - Training runs with metrics
   - Model artifacts
   - Feature importance plots

### Check GCS Bucket

```bash
# List files in GCS
gsutil ls gs://fin-data-bucket-115/model_output/

# Should see:
# - predictions_YYYYMM_*.csv
# - predictions_YYYYMM_*.parquet
# - summary_YYYYMM_*.json
```

## 🐛 Common Issues & Fixes

### Issue: ImportError for google.cloud.storage

```bash
# Fix: Install with explicit version
pip install google-cloud-storage==2.10.0
```

### Issue: W&B Login Failed

```bash
# Fix: Re-login with API key
wandb login --relogin
# Paste your API key from https://wandb.ai/authorize
```

### Issue: GCS Permission Denied

```bash
# Fix: Verify service account has correct role
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:YOUR_SA@PROJECT.iam.gserviceaccount.com" \
    --role="roles/storage.objectAdmin"
```

### Issue: FMP API Rate Limit

```bash
# Fix: Edit config.yaml
# Reduce concurrency from 8 to 4
api:
  concurrency: 4
```

### Issue: Module not found errors

```bash
# Fix: Run from correct directory
cd src/quantamental
python main.py --step all
```

## 🎓 For MS4 Submission

### Quick Checklist:

- [ ] All files in `src/quantamental/` directory
- [ ] `requirements.txt` present
- [ ] `config.yaml` configured
- [ ] README.md complete
- [ ] Tests written (next step)
- [ ] GitHub repo created
- [ ] CI/CD setup (next step)

### Next Steps (Day 4-5):

1. **Write Tests** (`tests/` folder)
2. **Setup GitHub Actions** (`.github/workflows/`)
3. **Create Documentation** (`docs/` folder)
4. **Take CI Screenshots**
5. **Submit commit hash**

## 📝 Development Workflow

### Daily Development Cycle

```bash
# 1. Pull latest data
python main.py --step collect --force-refresh

# 2. Process data
python main.py --step process

# 3. Train and experiment
python main.py --step train

# 4. Check W&B dashboard for results

# 5. Generate predictions
python main.py --step predict

# 6. Upload to GCS
python main.py --step backtest
```

### Weekly Production Run

```bash
# Automated weekly prediction (add to cron)
0 9 * * 1 cd /path/to/quantamental && python main.py --step all --skip-training >> /var/log/quantamental.log 2>&1
```

## 🔍 Debugging Tips

### Enable Verbose Logging

```python
# Add to top of any script
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components

```bash
# Test data collection only
python data_collect.py

# Test data processing only
python data_process.py

# Test model training only
python model_train.py
```

### Check W&B Logs

```python
import wandb
api = wandb.Api()
runs = api.runs("Quantamental-model")
print(f"Total runs: {len(runs)}")
for run in runs[:5]:
    print(f"{run.name}: {run.state}")
```

## Referemce

- **W&B **: https://docs.wandb.ai
- **GCS **: https://cloud.google.com/storage/docs
- **FMP **: https://financialmodelingprep.com/developer/docs

---

**Ready to start?** Run: `python main.py --step all`
