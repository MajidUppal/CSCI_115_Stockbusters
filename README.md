## AC215/CSCIE-115 - Milestone 4: A Multi-Agent System for Stock Recommendations

**Team Members** : Majid Uppal, Sirisom Pranivong, Seraphim Eilken, Mahmood Masqati

**Group Name**  Stock Busters

**What is new in MS4?**

This repository contains the development-ready version of the LLM-Powered Quantamental Stock Screener application for AC215/E115 Milestone 4.
Milestone 4 focuses on:

    - End-to-end local functionality

    - Clean code organization

    - Fully working backend APIs, agents, model, and frontend

    - Continuous Integration with automated tests

    - Data versioning and reproducibility

    - A deployment-ready codebase (for Cloud Run/Vertex AI in MS5)

### Project Milestone 4 - Code Organization

## please review your own section  - Seraphim /Majid/Mahmood/Siri ##

```
AC215_StockBusters/
│
├── src/
│   ├── quant-pipeline/              ← Your quantamental model, hybrid, backtest
│   │   ├── data_fetch.py
│   │   ├── data_preprocess.py
│   │   ├── feature_engineering.py
│   │   ├── model_train.py
│   │   ├── hybrid_score.py
│   │   ├── backtest.py
│   │   ├── export_outputs.py
│   │   ├── config.py
│   │   └── run_pipeline.py          ← final pipeline orchestrator
│   │
│   ├── api-service/                 ← FastAPI backend   
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── services/
│   │   ├── gcs_client.py
│   │   ├── model_loader.py
│   │   └── Dockerfile
│   │
│   ├── agent-orchestrator/           ← LLM multi-agent brain
│   │   ├── agent_controller.py
│   │   ├── planner_agent.py
│   │   ├── quant_agent.py
│   │   ├── rag_agent.py
│   │   ├── llm_client.py
│   │   └── Dockerfile
│   │
│   ├── rag-vector-db/                ← Chroma / PGVector
│   │   ├── build_index.py
│   │   ├── query_index.py
│   │   └── Dockerfile
│   │
│   ├── model-deploy/                 ← Vertex AI or Cloud Run infra
│   │   ├── deploy_model.py
│   │   ├── deploy_api.py
│   │   └── cloudbuild.yaml
│   │
│   ├── ml-workflow/                  ← Vertex AI pipelines (optional)
│   │   ├── pipeline.yaml
│   │   └── components/
│   │
│   ├── frontend-react/               ← React UI
│   │   ├── src/
│   │   ├── public/
│   │   └── package.json
│   │
│   └── notebooks/                    ← Your raw development notebooks
│       ├── Quantamental_MS4.ipynb
│       ├── RAG_Processing.ipynb
│       └── Agent_Prototype.ipynb
│
├── secrets/
│   └── service-account.json          ← for GCS
│
├── dvc.yaml                           ← data versioning
├── requirements.txt
├── README.md
└── .env.example
```



### Milestone4 : Development and Deployment ###

Milestone 4 focuses on integrating all components developed in previous milestones into a complete, working application. The goal is to make your system fully functional and testable locally, with clean code organization, automated testing, and continuous integration in place.

By the end of this milestone, your project should be deployment-ready — meaning that all components run reliably on your local environment and can be packaged or containerized for future cloud deployment.
Full cloud deployment and scalability considerations will be addressed in Milestone 5.



### Application Design Document ###              (Mahmood/Majid)

## Solution Architecture ## (Mahmood/Majid)
    < from MS4 requirement, please add   High-level overview of system components and their interactions (e.g., data flow, APIs, frontend, model). >  <-- delete this line once completed

## Technical Architecture ##  (Mahmood/Majid)

<from MS4 requirement please add Technologies, frameworks, and design patterns used, and how they support your overall system design.> <-- delete this line once completed

### APIs and Frontend Implementation ###  (Mahmood/Majid)

<from MS4 requirement please add 
Source code for both the backend APIs and the frontend interface, showing full end-to-end functionality.
Should include:
README: Setup instructions, environment configuration, and usage guidelines (how to run locally).
Repository Structure:
Organized and documented code following a consistent style guide (e.g., PEP 8 for Python, Airbnb for JS).
Clear separation of logic by domain (e.g., api/, models/, services/, ui/, tests/).
Comments or docstrings that clarify functionality and module purpose.  >


### Continuous Integration and Testing  ###   (Siri/Seraphim/Majid/Mahmood - please add example of CI of your own section) 

## Model CI Pipeline ##  (Siri)
    Set up a CI pipeline (e.g., GitHub Actions) that runs on every push and pull request.
    The pipeline must:
    Build and Lint: Perform automated build and code-quality checks (e.g., Flake8, ESLint).
    Run Tests: Execute all test suites (unit, integration, and end-to-end).
    Report Coverage: Generate and display code coverage reports (minimum 50%).



## RAG CI Pipeline & Evidence ##  (Seraphim)
    < from MS4-Set up a CI pipeline (e.g., GitHub Actions) that runs on every push and pull request.
    The pipeline must:
    Build and Lint: Perform automated build and code-quality checks (e.g., Flake8, ESLint).
    Run Tests: Execute all test suites (unit, integration, and end-to-end).
    Report Coverage: Generate and display code coverage reports (minimum 50%).  >

    CI Evidence:
    Screenshot(s) of a passing CI run showing:
    Successful build and linting
    All tests passing
    Code coverage report (minimum 50%)

## Front End CI Pipeline & Evidence ## (Mahmood)
    < from MS4-Set up a CI pipeline (e.g., GitHub Actions) that runs on every push and pull request.
    The pipeline must:
    Build and Lint: Perform automated build and code-quality checks (e.g., Flake8, ESLint).
    Run Tests: Execute all test suites (unit, integration, and end-to-end).
    Report Coverage: Generate and display code coverage reports (minimum 50%).  >

    CI Evidence:
    Screenshot(s) of a passing CI run showing:
    Successful build and linting
    All tests passing
    Code coverage report (minimum 50%)


## API CI pipeline ## (Majid)
    < from MS4-Set up a CI pipeline (e.g., GitHub Actions) that runs on every push and pull request.
    The pipeline must:
    Build and Lint: Perform automated build and code-quality checks (e.g., Flake8, ESLint).
    Run Tests: Execute all test suites (unit, integration, and end-to-end).
    Report Coverage: Generate and display code coverage reports (minimum 50%).  >

    CI Evidence:
    Screenshot(s) of a passing CI run showing:
    Successful build and linting
    All tests passing
    Code coverage report (minimum 50%)


## Data Versioning and Reproducibility##   (Siri)

    <MS4 : Implement and document your data versioning workflow (e.g., using DVC or an equivalent approach).
    Should include:
    The chosen method and a short justification for it. Version history for datasets or large artifacts (commits, tags, or snapshots).
    Instructions for data retrieval (dvc pull, push, or equivalent). If applicable, include LLM prompts and outputs for generated data. >

    

## Model Fine-Tuning## (Siri)
    Should include:
    Training scripts/config files, dataset references (versioned), and experiment logs.
    A concise summary of key results and how the fine-tuned model affects your deployment strategy.

    Data Versioning documentation (methodology, justification, and usage instructions)
    Model Training/Fine-Tuning summary (training process, results, and deployment implications)

























---
**2. Containerized Pipeline**

Build Dockerized components for ingestion, preprocessing, and RAG workflow.

Combine into a single runnable pipeline (docker compose up).

**Deliverables:**


The current version has two containers.
- Data pipeline container
- RAG container
  
These containers are build and run with single command as required through Docker Compose file. The docker compose file can be seen here at [compose.yml](https://github.com/Siri-Gith1/AC215_StockBusters/blob/Milestone2/compose.yml).
Run the compose.yml using the following command

`sudo docker compose up`

The UV dependency is handled by each individual container.

Below are snapshots for the Docker compose executed in the AC215_StockBusters.

***Docker Creation***
<img width="1688" height="1310" alt="image" src="https://github.com/user-attachments/assets/e624c591-ee41-4fb8-a6de-300033743d0c" />


<img width="1626" height="536" alt="image" src="https://github.com/user-attachments/assets/2ffe8d75-fdbf-4049-ab68-07a7d42ac6f1" />

Here the two containers working independently can be seen downloading the data for data pipeline while the RAG container is creating embeddings. 

<img width="1678" height="514" alt="image" src="https://github.com/user-attachments/assets/a5bac83c-7b20-47d1-9a9d-bd709fbc31f4" />



Below are the images of the created containers

<img width="1114" height="108" alt="image" src="https://github.com/user-attachments/assets/d5055582-738c-45b0-9049-9ae6eec6ea3f" />

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

**Update in Milestone 3** 
**Why We Moved Away from yfinance :**

In MS2, we considered using yfinance to download historical market data.
However, we faced two major issues:

- Rate limits: yfinance frequently blocks or throttles requests when fetching data for hundreds of tickers.

- Data quality: Some tickers had missing or inconsistent values, and certain delisted stocks returned incomplete histories.

To address this, we switched to Financial Modeling Prep (FMP) because it provides:

- Reliable OHLCV and fundamental data.

- Both quarterly and annual reports.

- Faster downloads using asynchronous requests (aiohttp).

- .parquet caching for speed and reproducibility.


This change significantly improved data completeness, speed, and reliability for our quantamental pipeline.

**2. Quantamental Model (Random Forest Classification)**
    
- Adding Quantamental Model (which is based on Random forest classification)

**3. Create Hybrid score for Stock ranking**

- Create Hybrid Score which combines the fundamental features and technical features together 

<img width="1902" height="673" alt="image" src="https://github.com/user-attachments/assets/efd50c36-4cd3-4eea-b9d5-0bf81e9c29ed" />


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
