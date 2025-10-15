## AC215/CSCIE-115 - Milestone 2: A Multi-Agent System for Stock Recommendations

**Team Members** : Majid Uppal, Sirisom Pranivong, Seraphim Eilken, Mahmood Masqati

**Group Name**  Stock Busters

### Project Milestone 2 Organization

** fill in the github structure here**
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
    │   ├── rag.py
    │   ├── Dockerfile
    │   ├── docker-compose.yml       # local-only
    │   ├── pyproject.toml
    │   ├── .env.example
    │   ├── README.md
    │   │
    │   ├── data/
    │   │   └── PrinciplesofFinanceSample.pdf
    │   │
    │   ├── artifacts/
    │   │   ├── ingest_summary.json
    │   │   ├── metadata.json
    │   │   └── retrieval_sample.json
    │   │
    │   └── volumes/
    │       └── chroma/
    │           ├── chroma.sqlite3
    │           └── [vector index bins]
    │
    ├── app_mockup/    
   



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







**2. Containerized Pipeline** **< Majid & mahmood>**

Build Dockerized components for ingestion, preprocessing, and RAG workflow.

Combine into a single runnable pipeline (docker compose up).

**Deliverables:**

Dockerfile for each component , pyproject.toml (with uv dependency manager) ,docker-compose.yml
and Logs and example I/O showing a complete run

< adding detail here>








**3. RAG pipeline**  **< Seraphim>**


Implement data collection, chunking, and vector database integration. Enable retrieval from financial text sources.

**Deliverables:**

- Containerized RAG modules (Ingest → Chunk → Embed → Store → Query)

- Evidence of working vector DB (Chroma/FAISS)

- Logs of successful retrieval and generation

< add detail here>
**RAG Workflow**

 < add detail here>








 **4. Finance Data ingestion** <Siri>

<Siri - data below is a placeholder only>

1. **`src/datapipeline/preprocess_cv.py`**
   This script handles preprocessing on our 100GB dataset. It reduces the image sizes to 128x128 (a parameter that can be changed later) to enable faster iteration during processing. The preprocessed dataset is now reduced to 10GB and stored on GCS.

2. **`src/datapipeline/preprocess_rag.py`**
   This script prepares the necessary data for setting up our vector database. It performs chunking, embedding, and loads the data into a vector database (ChromaDB).

3. **`src/datapipeline/Pipfile`**
   We used the following packages to help with preprocessing:
   - `special cheese package`

4. **`src/preprocessing/Dockerfile(s)`**
   Our Dockerfiles follow standard conventions, with the exception of some specific modifications described in the Dockerfile/described below.


**5. Application Mock-up**  < Mahmood>

(Explain and add snapshot here)


## System Architecture ## <Majid>

(Update detail and snapshot here)

