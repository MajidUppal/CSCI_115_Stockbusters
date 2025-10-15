"""
Finance Data Download & Upload Pipeline
---------------------------------------

This script:
1. Downloads an S&P 500 ticker list from Google Cloud Storage (GCS)
2. Fetches OHLCV data for all tickers using yfinance
3. Saves both wide (raw) and long format datasets locally
4. Uploads results back to the configured GCS bucket

Usage:
    export GOOGLE_APPLICATION_CREDENTIALS="secrets/service_account.json"
    python src/fin_data_download/data_download.py
"""

import pandas as pd
import numpy as np
import yfinance as yf
from google.cloud import storage
import os
import ta
from ta import add_all_ta_features
import requests

# ---------------------------
# GCP Configuration
# ---------------------------
BUCKET_NAME = "fin-data-bucket-115"
TICKER_FILE_GCS = "SP500_list.csv"  
LOCAL_TICKER_FILE = "SP500_list.csv"
RAW_LOCAL_FILE = "sp500_raw_data.csv"
LONG_LOCAL_FILE = "sp500_long_data.csv"
RAW_GCS_PATH = "sp500_raw_data.csv"
LONG_GCS_PATH = "sp500_long_data.csv"

# ---------------------------
#  GCS Utility Functions
# ---------------------------
def download_from_gcs(bucket_name, source_blob, destination_file):
    """Download file from GCS to local directory."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob)
    blob.download_to_filename(destination_file)
    print(f"🎉 Downloaded gs://{bucket_name}/{source_blob} → {destination_file}")


def upload_to_gcs(bucket_name, source_file, dest_blob):
    """Upload local file to GCS."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(dest_blob)
    blob.upload_from_filename(source_file)
    print(f"🎉 Uploaded {source_file} → gs://{bucket_name}/{dest_blob}")


# ---------------------------
#  Step 1: Download ticker list from GCS
# ---------------------------
print(" Downloading ticker list from GCS...")
download_from_gcs(BUCKET_NAME, TICKER_FILE_GCS, LOCAL_TICKER_FILE)

sp500_df = pd.read_csv(LOCAL_TICKER_FILE)
tickers = sp500_df["Symbol"].dropna().astype(str).unique().tolist()
tickers = [t.replace(".", "-") for t in tickers]

print(f"🎉 Loaded {len(tickers)} tickers from {LOCAL_TICKER_FILE}")

# ---------------------------
#  Step 2: Download historical data from yfinance
# ---------------------------
start_date = "2019-01-01"
end_date = "2025-09-30"

print(f"🎉 Downloading OHLCV data ({start_date} → {end_date}) for {len(tickers)} tickers...")
raw_data = yf.download(
    tickers,
    start=start_date,
    end=end_date,
    interval="1d",
    group_by="ticker",
    threads=True
)

raw_data.to_csv(RAW_LOCAL_FILE)
print(f"🎉 Saved raw wide-format data → {RAW_LOCAL_FILE}")

# ---------------------------
#  Step 3: Convert to long format
# ---------------------------
if isinstance(raw_data.columns, pd.MultiIndex):
    print(" Converting MultiIndex data to long format...")

    long_frames = []
    for ticker in tickers:
        try:
            df = raw_data[ticker].copy()
            df["Ticker"] = ticker
            df["Date"] = df.index
            long_frames.append(df)
        except KeyError:
            print(f" Skipped missing/malformed ticker: {ticker}")
            continue

    long_df = pd.concat(long_frames, axis=0).reset_index(drop=True)
    long_df = long_df.dropna(subset=["Close"])

    cols = ["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]
    long_df = long_df[[c for c in cols if c in long_df.columns]]

    long_df.to_csv(LONG_LOCAL_FILE, index=False)
    print(f"🎉 Saved long-format data → {LONG_LOCAL_FILE}")
    print(f"🎉 Successfully processed {long_df['Ticker'].nunique()} tickers.")
else:
    print(" Unexpected format: raw_data does not use MultiIndex. Check ticker list or retry smaller batch.")
    long_df = pd.DataFrame()

# ---------------------------
#  Step 3.5: Add Technical Indicators
# ---------------------------
try:
    print(" Adding technical indicators using TA library...")
    long_df = add_all_ta_features(
        long_df,
        open="Open",
        high="High",
        low="Low",
        close="Close",
        volume="Volume",
        fillna=True
    )
    print(f"🎉 Added {len(long_df.columns)} columns including TA features.")
except Exception as e:
    print(f" Skipped TA features due to error: {e}")


# ---------------------------
#  Step 4: Upload both CSVs to GCS
# ---------------------------
print(" Uploading files to GCS...")
upload_to_gcs(BUCKET_NAME, RAW_LOCAL_FILE, RAW_GCS_PATH)
upload_to_gcs(BUCKET_NAME, LONG_LOCAL_FILE, LONG_GCS_PATH)

print("\n🎉🎉 Pipeline completed successfully!🎉🎉")
