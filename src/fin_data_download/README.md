
# Milestone 2 — Finance Data Ingestion Pipeline (Docker + GCS)

This module implements a **containerized data ingestion pipeline** that downloads financial data (S&P 500 tickers and historical OHLCV data), processes it with Python, and uploads results to a Google Cloud Storage (GCS) bucket.  
It is part of the **CSCI-115 Stock Screener Project**, under the `Milestone2` branch.

---

## Overview

The pipeline automates:
1. Downloading the S&P 500 ticker list from a GCS bucket  
2. Fetching OHLCV (Open, High, Low, Close, Volume) data from Yahoo Finance  
3. Computing technical indicators using the `ta` library  
4. Saving processed data locally and uploading results back to GCS  

The entire workflow runs inside a **Docker container**, ensuring consistent environments across all team members.

---

##  Folder Structure
```text
Milestone2/
│
├── src/
│ └── fin_data_download/
│ ├── data_download.py # Main ingestion script
│ ├── gcs_utils.py # Helper utilities for GCS I/O
│ ├── requirements.txt # Python dependencies
│ ├── Dockerfile # Container build definition
│ └── .dockerignore # Excluded files from Docker context
│
├── notebooks/
│ └── finance_data_download.ipynb # Development notebook version
│
├── secrets/
│ └── service_account.json # GCP credentials (ignored by Git)
│
├── README.md # This documentation file
└── .gitignore # Ignore cache, venv, and secrets
```

##  Prerequisites

Before building the image, make sure you have:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed  
- Access to your team’s **Google Cloud Project**  
- A valid **service account JSON key** with permission to read/write the target GCS bucket  
- The environment variable `GOOGLE_APPLICATION_CREDENTIALS` pointing to that JSON file (set automatically in the Dockerfile)

---

##  GCS Setup

1. Create or use an existing bucket (e.g. `fin-data-bucket`).  
2. Upload your input CSVs to the bucket root (no subfolders), for example: gs://fin-data-bucket/SP500_list.csv
3. Place your service account key inside: Milestone2/secrets/service_account.json
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

