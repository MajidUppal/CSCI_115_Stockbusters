# RAG Reasoning Pipeline Integration

## Overview

The RAG (Retrieval-Augmented Generation) reasoning pipeline automatically generates investment reasoning for each stock in the quantamental pipeline output. It uses a financial knowledge base stored in ChromaDB to provide context-aware investment analysis.

## How It Works

### Integration Architecture

```
┌─────────────────────────────────────────────────────────┐
│  QUANTAMENTAL PIPELINE (Original, Unchanged)           │
│  ┌───────────────────────────────────────────────────┐  │
│  │ 1. Data Collection                                │  │
│  │ 2. Data Processing                                │  │
│  │ 3. Model Training                                 │  │
│  │ 4. Prediction                                     │  │
│  │ 5. Backtest & Create CSV                          │  │
│  │    → combined_quantamental_hybrid_with_...csv   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  REASONING PIPELINE (New Wrapper)                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │ 6. Load CSV from pipeline output                  │  │
│  │ 7. Connect to ChromaDB (RAG knowledge base)       │  │
│  │ 8. Generate reasoning for each stock:             │  │
│  │    - Extract key metrics (P/E, ROE, RSI, etc.)    │  │
│  │    - Query RAG system with stock data             │  │
│  │    - LLM generates investment reasoning           │  │
│  │ 9. Add 'rag_reasoning' column to CSV              │  │
│  │ 10. Upload enhanced CSV to GCS                    │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  OUTPUT: Enhanced CSV with Reasoning                    │
│  combined_quantamental_hybrid_with_factors_and_        │
│  backtest_with_reasoning.csv                            │
└─────────────────────────────────────────────────────────┘
```

## Components

### 1. Main Reasoning Module (`generate_stock_reasoning.py`)

**Purpose**: All-in-one script for generating investment reasoning using RAG system

**Key Functions**:
- `generate_reasoning_for_dataframe()` - Processes DataFrame and adds reasoning column
- `add_reasoning_to_combined_file()` - Reads CSV, adds reasoning, saves enhanced CSV
- `run_pipeline_with_reasoning()` - Wrapper that runs full pipeline and adds reasoning

**How It Works**:
1. Connects to ChromaDB (downloads from GCS)
2. Retrieves full financial knowledge base document (`.md` file)
3. Sets up LLM (Gemini 2.5 Flash) with RAG chain
4. For each stock:
   - Extracts key metrics (symbol, scores, ratios, sector, etc.)
   - Creates compact query string
   - Sends to LLM with knowledge base context
   - Receives investment reasoning
5. Adds `rag_reasoning` column to DataFrame

**Execution Modes**:
- **Standalone Mode**: Process existing CSV files (downloads from GCS or uses local file)
- **Pipeline Mode**: Run full quantamental pipeline and automatically add reasoning after backtest

**Key Features**:
- Calls original pipeline functions (unchanged)
- After backtest completes, adds reasoning to CSV
- Re-uploads enhanced CSV to GCS
- Non-invasive: No original files modified
- Supports both standalone CSV processing and full pipeline integration

## Usage

**⚠️ IMPORTANT: Choose the right command for your use case below**

---

## 🚀 Quick Start Commands

### Option 1: Run Full Pipeline WITH Reasoning ⭐ (Recommended)

**What it does**: Runs the complete quantamental pipeline (data collection → processing → training → prediction → backtest) AND automatically adds investment reasoning to the output CSV.

**Local Execution:**
```bash
cd src/quantamental
python generate_stock_reasoning.py --mode pipeline --step all
```

**Docker Execution:**
```bash
docker run --rm \
  -v "${PWD}\..\..\secrets:/app/secrets" \
  quantamental-reasoning \
  python generate_stock_reasoning.py --mode pipeline --step all
```

**Output**: Enhanced CSV uploaded to GCS with `rag_reasoning` column added.

---

### Option 2: Run Pipeline WITHOUT Reasoning (Original Pipeline)

**What it does**: Runs the complete quantamental pipeline but DOES NOT add reasoning. This is the original pipeline behavior.

**Local Execution:**
```bash
cd src/quantamental
python main.py --step all
```

**Docker Execution:**
```bash
docker run --rm \
  -v "${PWD}\..\..\secrets:/app/secrets" \
  quantamental-reasoning \
  python main.py --step all
```

**Output**: Standard CSV uploaded to GCS (no `rag_reasoning` column).

**Alternative**: You can also use the reasoning script with `--disable-rag` flag:
```bash
python generate_stock_reasoning.py --mode pipeline --step all --disable-rag
```

---

### Option 3: Run ONLY Reasoning (Standalone Mode)

**What it does**: Processes an existing CSV file (from GCS or local) and adds reasoning WITHOUT running the full pipeline. Useful when you already have a CSV and just want to add reasoning to it.

**Local Execution:**
```bash
cd src/quantamental

# Process all stocks from GCS (default input file)
python generate_stock_reasoning.py --mode standalone

# Process local CSV file
python generate_stock_reasoning.py --mode standalone --csv-path ./data/combined_file.csv

# Test with sample of 10 stocks (faster)
python generate_stock_reasoning.py --mode standalone --sample-size 10

# Adjust parallel workers for faster processing
python generate_stock_reasoning.py --mode standalone --max-workers 30
```

**Docker Execution:**
```bash
# Process all stocks from GCS
docker run --rm \
  -v "${PWD}\..\..\secrets:/app/secrets" \
  quantamental-reasoning \
  python generate_stock_reasoning.py --mode standalone

# Process with sample size
docker run --rm \
  -v "${PWD}\..\..\secrets:/app/secrets" \
  quantamental-reasoning \
  python generate_stock_reasoning.py --mode standalone --sample-size 10

# Process with custom max workers
docker run --rm \
  -v "${PWD}\..\..\secrets:/app/secrets" \
  quantamental-reasoning \
  python generate_stock_reasoning.py --mode standalone --max-workers 30
```

**Output**: Enhanced CSV uploaded to GCS with `rag_reasoning` column added.

---

## 📋 Additional Command Options

### Pipeline Mode Options

```bash
# Run only the backtest step with reasoning
python generate_stock_reasoning.py --mode pipeline --step backtest

# Skip training (use existing model)
python generate_stock_reasoning.py --mode pipeline --step all --skip-training

# Force refresh data from API
python generate_stock_reasoning.py --mode pipeline --step all --force-refresh

# Run pipeline but disable reasoning generation
python generate_stock_reasoning.py --mode pipeline --step all --disable-rag
```

### Standalone Mode Options

```bash
# Process specific number of stocks (for testing)
python generate_stock_reasoning.py --mode standalone --sample-size 50

# Use more parallel workers (faster but may hit rate limits)
python generate_stock_reasoning.py --mode standalone --max-workers 40

# Process local CSV file instead of downloading from GCS
python generate_stock_reasoning.py --mode standalone --csv-path ./output/my_file.csv

# Combine options
python generate_stock_reasoning.py --mode standalone --sample-size 20 --max-workers 15
```

### Step Options for Pipeline Mode

Available steps: `collect`, `process`, `train`, `predict`, `backtest`, `all`

```bash
# Run specific step only
python generate_stock_reasoning.py --mode pipeline --step backtest

# Run multiple steps (example: data collection through training)
# Note: Steps must be run in order, so use --step all for complete pipeline
```

---

## 📊 Command Comparison Summary

| Use Case | Command | Output Location |
|----------|---------|----------------|
| **Full pipeline WITH reasoning** | `generate_stock_reasoning.py --mode pipeline --step all` | GCS: `model_output/..._with_reasoning.csv` |
| **Full pipeline WITHOUT reasoning** | `main.py --step all` | GCS: `model_output/...csv` (no reasoning) |
| **ONLY reasoning** (existing CSV) | `generate_stock_reasoning.py --mode standalone` | GCS: `model_output/..._with_reasoning.csv` |

---

## 🔍 Verifying Output

After running, verify the reasoning was added:

**Check GCS:**
- With reasoning: `gs://fin-data-bucket-115/model_output/combined_quantamental_hybrid_with_factors_and_backtest_with_reasoning.csv`
- Without reasoning: `gs://fin-data-bucket-115/model_output/combined_quantamental_hybrid_with_factors_and_backtest.csv`

**Download and verify locally:**
```bash
# Download the enhanced CSV
gsutil cp gs://fin-data-bucket-115/model_output/combined_quantamental_hybrid_with_factors_and_backtest_with_reasoning.csv ./

# Check that rag_reasoning column exists
python -c "import pandas as pd; df = pd.read_csv('combined_quantamental_hybrid_with_factors_and_backtest_with_reasoning.csv'); print(f'Columns: {list(df.columns)}'); print(f'Has reasoning: {\"rag_reasoning\" in df.columns}'); print(f'Non-empty reasoning: {df[\"rag_reasoning\"].notna().sum()}/{len(df)}')"
```

---

## Configuration

Edit `config.yaml`:

```yaml
rag:
  enabled: true        # Enable/disable reasoning generation
  max_workers: 20      # Parallel workers (default: 20)
  sample_size: null    # Optional: test with N stocks only (null = all stocks)
```

**Examples**:
```yaml
# Enable reasoning for all stocks
rag:
  enabled: true
  max_workers: 20
  sample_size: null

# Disable reasoning
rag:
  enabled: false

# Test with 10 stocks only
rag:
  enabled: true
  sample_size: 10
```

## What Gets Generated

### Input (from Quantamental Pipeline)
- `combined_quantamental_hybrid_with_factors_and_backtest.csv`
- Contains: symbol, scores, metrics, signals, etc.

### Output (Enhanced CSV)
- `combined_quantamental_hybrid_with_factors_and_backtest_with_reasoning.csv`
- Contains: All original columns + `rag_reasoning` column
- Example reasoning: *"Attractive P/E ratio. Strong RSI momentum. Solid ROE indicates efficient capital use."*

## Technical Details

### RAG System Components

1. **ChromaDB** (Vector Store)
   - Location: GCS bucket `stock-busters-chroma-bucket`
   - Contains: Embedded financial knowledge base (`.md` file)
   - Collection: `stocks_rag_v1`

2. **Embeddings**
   - Model: `BAAI/bge-small-en-v1.5` (384 dimensions)
   - Library: FastEmbed

3. **LLM**
   - Model: Gemini 2.5 Flash (Vertex AI)
   - Project: `stock-busters-cs115`

4. **Knowledge Base**
   - Source: Financial analysis document (`.md` file)
   - Content: Investment metrics, ratios, analysis guidelines
   - Storage: Single embedding in ChromaDB (full document)

### Processing Flow

1. **Setup Phase** (~10-15 seconds)
   - Download ChromaDB from GCS
   - Retrieve full knowledge base document
   - Initialize LLM and RAG chain
   - Cache document content locally

2. **Processing Phase** (~3-4 minutes for 390 stocks)
   - Parallel processing with 20 workers (configurable)
   - Each stock: ~0.6 seconds average
   - LLM generates reasoning based on:
     - Stock metrics (P/E, ROE, RSI, scores, etc.)
     - Financial knowledge base context
     - Investment analysis guidelines

3. **Output Phase** (~5 seconds)
   - Add `rag_reasoning` column to DataFrame
   - Save enhanced CSV locally
   - Upload to GCS

### Performance

- **Total Time**: ~3-4 minutes for 390 stocks
- **Per Stock**: ~0.6 seconds average
- **Parallelization**: 20 concurrent workers (default)
- **Token Efficiency**: 
  - Knowledge base in system message (cached by LLM)
  - Stock data in user message (~100-200 chars per stock)

## File Structure

```
src/
├── quantamental/
│   ├── main.py                    # Original pipeline (unchanged)
│   ├── backtest.py                # Original backtest (unchanged)
│   ├── generate_stock_reasoning.py # All-in-one reasoning script (includes RAG helpers + standalone + pipeline modes)
│   ├── config.yaml                # Configuration (includes RAG settings)
│   ├── Dockerfile                 # Docker config (includes reasoning files)
│   ├── requirements.txt           # Dependencies (includes RAG packages)
│   └── REASONING_PIPELINE.md      # This file
```

**Note**: All reasoning functionality, including RAG helper functions (ChromaDB connection, embeddings, etc.), is consolidated in `generate_stock_reasoning.py` for simplicity and maintainability.

## Dependencies

Required packages (should be in `requirements.txt`):
```
pandas
google-cloud-storage
google-auth
langchain-google-vertexai
langchain-community
langchain-core
python-dotenv
chromadb
fastembed
tqdm
```

## Credentials

The system automatically searches for credentials in:
1. `secrets/stock-busters-service-account.json`
2. `../secrets/stock-busters-service-account.json`
3. Environment variable `GOOGLE_APPLICATION_CREDENTIALS`

## Error Handling

- **If reasoning fails**: Pipeline continues, CSV uploaded without reasoning column
- **If ChromaDB unavailable**: Error logged, pipeline continues
- **If LLM rate limit**: Errors logged per stock, others continue processing

## Example Output

### Input CSV Row
```csv
symbol,signal,Hybrid_Score,Fundamental_Score,Technical_Score,roe,peRatio,RSI_14,sector,industry
AAPL,1,0.85,0.82,0.88,0.45,28.5,65.2,Technology,Consumer Electronics
```

### Output CSV Row (with reasoning)
```csv
symbol,signal,Hybrid_Score,...,rag_reasoning
AAPL,1,0.85,...,Strong fundamental metrics with attractive valuation. High technical momentum. Solid ROE indicates efficient capital allocation. Technology sector positioning favorable.
```

## Troubleshooting

### Reasoning Not Generated

**Check**:
1. `rag.enabled: true` in `config.yaml`
2. Credentials file exists in `secrets/`
3. ChromaDB bucket accessible: `stock-busters-chroma-bucket`
4. Vertex AI access enabled

### Slow Processing

**Solutions**:
- Increase `max_workers` (default: 20)
- Check network connection to Vertex AI
- Verify ChromaDB cache is working (check `.chromadb_full_doc_cache.json`)

### Import Errors

**Solution**: All RAG helper functions are now in `generate_stock_reasoning.py`. No separate `rag_helpers.py` file is needed.

## Integration Points

### Where Reasoning Runs

1. **Trigger**: After quantamental pipeline's backtest step completes (when using pipeline mode)
2. **Input**: CSV file created by `backtest.py` → `create_agent_output_files()`
3. **Processing**: `generate_stock_reasoning.py` → `generate_reasoning_for_dataframe()`
4. **Output**: Enhanced CSV uploaded to GCS

### Non-Invasive Design

✅ **No original files modified**:
- `main.py` - Unchanged
- `backtest.py` - Unchanged
- All other pipeline files - Unchanged

✅ **Wrapper approach**:
- `generate_stock_reasoning.py` in pipeline mode calls original functions from `main.py`
- Adds reasoning step after pipeline completes
- Original pipeline (`main.py`) still works independently
- Can also be used standalone to process existing CSV files

## Next Steps

### Quick Testing

1. **Test reasoning generation with a small sample**:
   ```bash
   python generate_stock_reasoning.py --mode standalone --sample-size 10
   ```

2. **Run full pipeline with reasoning**:
   ```bash
   python generate_stock_reasoning.py --mode pipeline --step all
   ```

### Production Deployment

1. **Configure** (optional):
   - Edit `config.yaml` to set `rag.enabled: true`
   - Adjust `max_workers` for optimal performance

2. **Run full pipeline with reasoning**:
   - Local: `python generate_stock_reasoning.py --mode pipeline --step all`
   - Docker: Use Docker commands from [Quick Start](#-quick-start-commands) section

3. **Verify output**:
   - Check GCS: `gs://fin-data-bucket-115/model_output/combined_quantamental_hybrid_with_factors_and_backtest_with_reasoning.csv`
   - Verify `rag_reasoning` column exists and is populated
   - Review reasoning quality for a few stocks

### Docker Deployment

All commands work in Docker with the same arguments:

```bash
# Build image
docker build -t quantamental-reasoning -f src/quantamental/Dockerfile src/quantamental

# Run full pipeline with reasoning
docker run --rm \
  -v "${PWD}/secrets:/app/secrets" \
  quantamental-reasoning \
  python generate_stock_reasoning.py --mode pipeline --step all

# Run only reasoning (standalone)
docker run --rm \
  -v "${PWD}/secrets:/app/secrets" \
  quantamental-reasoning \
  python generate_stock_reasoning.py --mode standalone
```

## Summary

### Three Main Ways to Use This System

1. **Run Full Pipeline WITH Reasoning** ⭐
   - Command: `python generate_stock_reasoning.py --mode pipeline --step all`
   - Runs complete pipeline + automatically adds reasoning to output
   - Best for: Production runs, end-to-end pipeline execution

2. **Run Pipeline WITHOUT Reasoning**
   - Command: `python main.py --step all`
   - Runs original pipeline only (no reasoning added)
   - Best for: When you don't need reasoning, faster execution

3. **Run ONLY Reasoning (Standalone)**
   - Command: `python generate_stock_reasoning.py --mode standalone`
   - Processes existing CSV and adds reasoning only
   - Best for: Adding reasoning to previously generated CSVs, testing reasoning quality

### Key Features

- **Seamless Integration**: Reasoning runs automatically after pipeline completes (pipeline mode)
- **Standalone Processing**: Can process existing CSVs independently (standalone mode)
- **Investment Reasoning**: Uses RAG system with financial knowledge base
- **Non-Invasive**: No original pipeline files modified
- **Configurable**: Easy to enable/disable via config.yaml or command flags
- **Efficient**: Parallel processing (20 workers default), optimized prompts
- **Reliable**: Error handling, continues on individual stock failures
- **Docker-Ready**: All files and dependencies included in Dockerfile
- **Caching**: ChromaDB document cached locally for faster subsequent runs
- **GCS Integration**: Automatically uploads enhanced CSV to GCS

### Output Files

- **With Reasoning**: `combined_quantamental_hybrid_with_factors_and_backtest_with_reasoning.csv`
  - Location: GCS `model_output/` folder
  - Contains: All original columns + `rag_reasoning` column
  
- **Without Reasoning**: `combined_quantamental_hybrid_with_factors_and_backtest.csv`
  - Location: GCS `model_output/` folder
  - Original pipeline output (no reasoning column)

The enhanced CSV with reasoning is ready for use by downstream systems (agents, APIs, dashboards).

## Implementation Notes

**All code is in `generate_stock_reasoning.py`**:
- RAG helper functions (ChromaDB connection, embeddings, query functions)
- Standalone mode functions (process CSV files)
- Pipeline mode functions (integrate with quantamental pipeline)
- RAG setup and reasoning generation
- GCS upload/download utilities

**Note**: The `rag_helpers.py` file has been merged into `generate_stock_reasoning.py` for simplicity. All ChromaDB connection and RAG query functionality is now in a single file.

**Key Design Decisions**:
1. Single file for all reasoning functionality (easier to maintain)
2. Two execution modes (standalone vs pipeline)
3. Original pipeline files untouched (non-invasive)
4. Configuration-driven (enable/disable via config.yaml)
5. Docker-compatible (all dependencies and files included)

