
# Milestone 2 — Finance Data Ingestion Pipeline (Docker + GCS)

This module builds an **end-to-end finance data ingestion pipeline** for the StockBusters project.  
It automatically downloads **S&P 500 stock data** from Yahoo Finance, computes **technical indicators**,  
and uploads the processed datasets directly to **Google Cloud Storage (GCS)** — with **no local file storage** required.

The pipeline performs the following tasks:

1. **Download the S&P 500 ticker list** from a designated GCS bucket.  
2. **Fetch OHLCV data** (Open, High, Low, Close, Volume) for all tickers using `yfinance`, in parallelized chunks.  
3. **Transform** raw data from wide to long format.  
4. **Enhance** each ticker’s time series with over 90 **technical indicators** (SMA, RSI, MACD, ATR, MFI, etc.) using the `ta` library.  
5. **Filter core features** relevant for modeling (trend, momentum, volatility, volume).  
6. **Upload final datasets** back to the GCS bucket in CSV format.

This module implements a **containerized data ingestion pipeline** that downloads financial data (S&P 500 tickers and historical OHLCV data), processes it with Python, and uploads results to a Google Cloud Storage (GCS) bucket.  

---

##  Folder Structure
```text
AC215_StockBusters/
│
├── src/
│ └── fin_data_download/
│ ├── data_download.py # Main ingestion script
│ ├── gcs_utils.py # Helper utilities for GCS I/O
│ ├── requirements.txt # Python dependencies
│ ├── Dockerfile # Container build definition
│ └── .dockerignore # Excluded files from Docker context
│ └── README.md # This documentation
│ └── pyproject.toml
│
├── notebooks/
│ └── finance_data_download.ipynb # Development notebook version
│
│
├── README.md # This documentation 
└── .gitignore # Ignore cache, venv, and secrets
```

##  Prerequisites

Before building the image, make sure you have:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed  
- Access to the team’s **Google Cloud Project**  
- A valid **service account JSON key** with permission to read/write the target GCS bucket  
- The environment variable `GOOGLE_APPLICATION_CREDENTIALS` pointing to that JSON file 

---

##  GCS Setup

1. Create or use an existing bucket (e.g. `fin-data-bucket-115`).  
2. Upload the input CSVs to the bucket root Ex. gs://fin-data-bucket/SP500_list.csv  This file contains the list of S&P500
3. Place your service account key outside: Milestone2/secrets/service_account.json
4. **Do not commit this file** — the `secrets/` folder is ignored by `.gitignore`.

##  Build and Run with Docker

From the project root:

```bash
# Build the image
docker build -f src/fin_data_download/Dockerfile -t fin-data-pipeline .

# Run the container, mounting your local secrets folder
docker run -v "${PWD}/secrets:/app/secrets" fin-data-pipeline

The container will:

1. Download the ticker list from GCS

2. Fetch historical OHLCV data via yfinance (5 years)

3. Compute technical indicators

4. Upload processed file back to the same GCS bucket

5. Fetch the income statement and balance sheet and upload to the same GCS bucket

