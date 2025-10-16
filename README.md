## AC215/CSCIE-115 - Milestone 2: A Multi-Agent System for Stock Recommendations

**Team Members** : Majid Uppal, Sirisom Pranivong, Seraphim Eilken, Mahmood Masqati

**Group Name**  Stock Busters

### Project Milestone 2 Organization


```
AC215_StockBusters/
│
├── .gitignore
├── LICENSE
├── README.md                     
│
├── docker-compose.yml             
│
├── data/
│   └── .gitkeep
│
├── notebooks/
│   ├── .gitkeep
│   └── Finance_data_download.ipynb
│
├── reference/
│   ├── .gitkeep
│   └── A Multi-Agent System for Stock Recommendations_MS1.pdf
│   └── Stock Busters App Wireframe.pdf
│
└── src/
    ├── fin_data_download/
    │   ├── data_download.py
    │   ├── gcs_utils.py
    │   ├── Dockerfile
    │   ├── pyproject.toml
    │   ├── requirements.txt
    │   ├── README.md
    │   └── .dockerignore
    │
    ├── rag/
    │   ├── rag.py # SINGLE Python file (CLI + pipeline + API)
    │   ├── Dockerfile # single image for ingest + serve
    │   ├── _archived/
    │   │ └── docker-compose.yml # legacy local-only compose file
    │   ├── pyproject.toml # runtime dependencies
    │   ├── .env # local config
    │   ├── uv.lock # uv lock file
    │   ├── README.md # RAG-specific README
    │   │
    │   ├── data/ # source docs (.pdf, .txt, .md)
    │   │ └── PrinciplesofFinanceSample.pdf
    │   │
    │   ├── artifacts/ # pipeline outputs
    │   │ ├── sanitized/ # cleaned text chunks
    │   │ ├── ingest_summary.json # chunking summary
    │   │ ├── metadata.json # metadata about ingested docs
    │   │ ├── retrieval_sample.json # optional retrieval sample
    │   │ └── sample_vector.json # optional sample embedding dump
    │   │
    │   ├── screenshot_logs/ # build/run/query logs
    │   │
    │   └── volumes/
    │   └── chroma/ # persisted Chroma store
    │   ├── chroma.sqlite3
    │   └── [vector index bins]
    │
        
   



```


### Project ###

The A Multi-Agent System for Stock Recommendations is an AI-driven, multi-agent system designed to integrate quantitative and fundamental financial data with expert-inspired reasoning. The system generates explainable stock recommendations tailored to individual investors’ goals and risk profiles.

In Milestone 2, our focus is on building the MLOps infrastructure that powers this system — containerizing all major components to ensure reproducibility, scalability, and modular deployment.

### Milestone2 : MLOps Infrastructure and ML Components ###

**1. Virtual Environment Setup**    **< Majid & mahmood>**

- Create and document working environments (local & cloud-based).

- Demonstrate successful containerized runs.

**Deliverable: Screenshot of running container instances.**

< adding detail here >






---
**2. Containerized Pipeline** **< Majid & mahmood>**

Build Dockerized components for ingestion, preprocessing, and RAG workflow.

Combine into a single runnable pipeline (docker compose up).

**Deliverables:**

Dockerfile for each component , pyproject.toml (with uv dependency manager) ,docker-compose.yml
and Logs and example I/O showing a complete run

< adding detail here>






---
**3. RAG pipeline**  


Implement data collection, chunking, and vector database integration. Enable retrieval from financial text sources.

**Deliverables:**

- **Containerized RAG modules** (Ingest → Chunk → Embed → Store → Query)  
  *Location*: `src/rag/rag.py`  
- **Evidence of working vector DB** (Chroma with FastEmbed embeddings)  
  *Locations*: `src/rag/volumes/chroma/`, `src/rag/artifacts/sample_vector.json`
- **Logs of successful ingestion, retrieval, and API queries**  
  *Locations*: `src/rag/artifacts/` (`ingest_summary.json`, `retrieval_sample.json`, etc.), `src/rag/artifacts/sanitized` (chuncks),     
- **Screenshots of build, run, and query steps**  
  *Location*: `src/rag/screenshot_logs/`  
- **Documentation** (`README.md`, `Dockerfile`, Quick Start guide)  
  *Location*: `src/rag/README.md`

---
**RAG Workflow**

**Ingest**
- Documents from `rag/data/` (PDF, TXT, MD) are loaded.  
- Text is sanitized (removal of BOM, unicode normalization, whitespace cleanup).  
- Outputs written to `artifacts/sanitized/`.  

**Chunking**
- Text split into overlapping windows.  
- Metadata (chunk counts, sizes) recorded in `src/rag/artifacts/chunk_stats.json`.  

**Embedding**
- Each chunk is encoded using **FastEmbed** with the `BAAI/bge-small-en-v1.5` model.  
- Embedding dimension: 384.  
- Sample vector dump available in `src/rag/artifacts/sample_vector.json`.  

**Vector Storage**
- Chunks + embeddings stored in **Chroma** (`src/rag/volumes/chroma/`).  
- Collection name configurable via `.env` (default: `stocks_rag_v1`).  
- Database persists across runs for reproducibility.  

**Query (API)**
- FastAPI server runs inside the container (`API_PORT=8000`).  
- Exposes `/query` endpoint for semantic retrieval. 



---

 **4. Finance Data ingestion** 
 
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

---
**5. Stock Busters Mock-up App Description:`**

The Stock Busters application is designed as an agentic, mobile-first interface to demonstrate a financial analysis tool powered by AI. Its core function is to guide users through complex financial screening processes via a multi-step conversational flow.

Core Features:
Agentic Chat Interface: The app uses a conversational design to simulate an intelligent agent, replacing complex forms with simple dialogue. The agent asks clarifying questions (e.g., confirming the time horizon for "positive momentum") to refine the user's initial query before generating results.

**5-Step Conversational Flow: The wireframe demonstrates a full user journey:**

- Agent Greeting

- User Initial Query (e.g., "Find large-cap tech stocks...")

- Agent Clarification (Asking for missing criteria)

- User Response (Providing the final criteria)

- Final Results: A structured output with a stock table, fundamental data (ROE, Sector, Price Change), backtesting insights (CAGR, Max Drawdown), and detailed explanations.

<img width="1210" height="596" alt="image" src="https://github.com/user-attachments/assets/e10bf308-512d-43be-812f-77f27d4e64e5" />

Side Menu Navigation: A hidden menu provides access to auxiliary functions: Recent Searches (to review past queries), Settings (to manage preferences), and About (including a legal disclaimer).

<img width="1001" height="577" alt="image" src="https://github.com/user-attachments/assets/8d81c4c5-52cd-4fc8-bcfa-fa76bcfea0bc" />


The primary goal of this wireframe is to visually communicate the seamless, iterative nature of a sophisticated AI model that uses clarification to deliver precise, data-driven financial recommendations.

---
**6. Solution Architecture:**

<img width="1111" height="618" alt="image" src="https://github.com/user-attachments/assets/a762852b-40cd-4835-b4be-20dda83105e9" />

The architecture is designed to support application development, AI/ML tasks, and a Chat Bot feature, heavily leveraging Large Language Models (LLMs) like Gemini.

**1. Process Layer**

This is the user and high-level function layer, representing the main areas of interaction and functionality supported by the system:

**Develop App:** Standard application development activities, interacting with the Execution and State layers.

**AI/ML Tasks:** Functions related to the core AI/ML capabilities, such as model development and training.

**Chat Bot:** The conversational interface for users, likely a key feature of the Stock Busters app, which involves "Human Interactions."

**2. Execution Layer**

This layer contains the runtime components and services that handle the application's logic, processing, and user interaction:

**Interactive Notebooks (Notebooks):** Used for human interaction, likely by data scientists or developers, for experimentation and development of AI/ML models. These connect to LLMs and the State layer.

**ML Pipeline:** An automated process for managing the entire machine learning lifecycle:

**Data Collector:** Gathers necessary data.

**Model Training:** The core process of generating the AI/ML model.

**Data Processor:** Prepares data for training or inference.

**Model Deploy:** Puts the trained model into a production environment.

It's driven by CLI + Automation and interacts with LLMs.

**LLMs (as a Service) - Gemini:** A central service providing Large Language Model capabilities (like Gemini) via HTTP/HTTPS. It acts as a bridge between the Notebooks, ML Pipeline, and the Backend.

**Frontend (StockBusters):** The user-facing component of the main application, supporting "Human Interactions" and communicating with the Backend via HTTP/HTTPS.

**Backend:** The core application logic and data-handling services, accessible via HTTPS.

**API Service:** Handles business logic and serves the Frontend and LLMs.

**Vector DB Service:** Provides a vector database, essential for modern AI applications, particularly those utilizing LLMs (like for retrieval-augmented generation in the Chat Bot).

**3. State Layer**

This is the data and infrastructure layer that stores, manages, and tracks all persistent assets and data:

**Source Control:** Stores all application code, configuration, and potentially pipeline definitions.

**Artifact Registry:** Stores built artifacts, such as trained models from the ML Pipeline and other reusable components.

**Data Store:** Stores raw, processed, and training data utilized by the ML Pipeline and LLMs.

**Knowledge Base:** Stores structured and unstructured information (likely financial or market data) that the Backend, particularly the Vector DB Service, and LLMs can query to inform the application and Chat Bot responses.
