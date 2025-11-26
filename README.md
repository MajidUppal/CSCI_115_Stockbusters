## AC215/CSCIE-115 - Milestone 4: A Multi-Agent System for Stock Recommendations

**Team Members** : Majid Uppal, Sirisom Pranivong, Seraphim Eilken, Mahmood Masqati

**Group Name**  Stock Busters

**What is new in MS4?**

This repository contains the development-ready version of the LLM-Powered Quantamental Stock Screener application for AC215/E115 Milestone 4.
Milestone 4 focuses on:

- End-to-end local functionality

- Code organization

- Fully working backend APIs, agents, model, and frontend

- Continuous Integration with automated tests

- Data versioning and reproducibility

- A deployment-ready codebase (for Cloud Run/Vertex AI in MS5)

### Project Milestone 4 - Code Organization



```
AC215_StockBusters/
│
├──  README.md                    # Project documentation
├──  compose.yml                  # Docker Compose configuration
├──  .pre-commit-config.yaml      # Pre-commit hooks
│
├── .github/
│   └── workflows/
│       ├── quantamental-ci.yml     # Quantamental CI pipeline
│       └── ci-rag.yml              # RAG CI pipeline
│
├── 📁 docs/
│   └── CI_PIPELINE.md              # CI/CD documentation
│
├── 📁 coverage/                    # Test coverage reports
│
└── 📁 src/
    │
    ├── 📁 quantamental/            # ML Pipeline (Main Component)
    │   ├── Dockerfile
    │   ├── README.md
    │   ├── config.yaml             # Pipeline configuration
    │   ├── requirements.txt
    │   │
    │   ├── # Core Pipeline Scripts
    │   ├── main.py                 # Quantamental Main Pipeline orchestration (7 steps)
    │   ├── data_collect.py         # FMP API data collection
    │   ├── data_process.py         # Feature engineering
    │   ├── model_train.py          # Random Forest training
    │   ├── model_predict.py        # Prediction generation
    │   ├── model_validation.py     # Model Quality gates
    │   ├── hybrid_scoring.py       # Technical + fundamental scoring calculation 
    │   ├── backtest.py             # Backtesting & output
    │   ├── data_versioning.py      # W&B artifact versioning
    │   ├── generate_stock_reasoning.py  # RAG reasoning integration
    │   └── utils.py                # Utility functions
    │   │
    │   ├── 📁 tests/               # Test suite (130+ tests)
    │   │   ├── conftest.py         # Pytest fixtures
    │   │   ├── test_unit_*.py      # Unit tests
    │   │   ├── test_integration_*.py   # Integration tests
    │   │   ├── test_system_*.py    # System tests
    │   │   └── test_model_performance.py  # Validation tests
    │   │
    │   └── 📁 data/                # Local data directory
    │       └── version_info_*.json # Version metadata
    │
    ├── 📁 rag/                     # RAG Service
    │   ├── Dockerfile
    │   ├── docker-entrypoint.sh
    │   ├── pyproject.toml
    │   ├── pytest.ini
    │   ├── README.md
    │   ├── rag.py                  # RAG core functionality
    │   ├── generate_stock_reasoning.py
    │   │
    │   ├── 📁 data/
    │   │   └── LLM-Quant_Expanded_RAG_with_context.md
    │   │
    │   ├── 📁 docs/
    │   │   ├── APPLICATION_DESIGN.md
    │   │   ├── CONTINUOUS_INTEGRATION_PIPELINE.md
    │   │   └── DATA_VERSIONING.md
    │   │
    │   └── 📁 tests/
    │       ├── unit/               # Unit tests
    │       ├── integration/        # Integration tests
    │       └── system/             # System tests
    │
    ├── 📁 api-service/             # FastAPI Backend
    │   ├── Dockerfile
    │   │
    │   ├── 📁 api/
    │   │   ├── service.py          # Main FastAPI app
    │   │   ├── utils.py
    │   │   │
    │   │   ├── 📁 routers/
    │   │   │   ├── chatbot_final.py
    │   │   │   └── stock_details.py
    │   │   │
    │   │   └── 📁 utils/
    │   │       ├── chat_bot_agent.py
    │   │       ├── detailed_page_funcs.py
    │   │       └── get_gcs_bucket.py
    │   │
    │   └── 📁 tests/               # API tests
    │
    ├── 📁 frontend/                # ⚛️ React Frontend
    │   │   ├── app/
    │   │   │   ├── chat/           # Chat interface
    │   │   │   ├── report/         # Stock reports
    │   │   │   ├── stock-detail/   # Stock detail pages
    │   │   │   ├── settings/       # User settings
    │   │   │   ├── page            # Home page
    │   │   │   └── layout          # Header, Footer, Theme
    │   │   │
    │   │   ├── components          # components for corresponding app pages plus share ui component
    │   │   ├── lib/
    │   │       ├── DataService.js  # API integration
    │   │       ├── Common.js
    │   │       └── utils.js
    │   ├── .env.development│   
    │   ├── Dockerfile
    │   ├── docker-shell.sh 
    │   └── README.md
    │
    └── 📁 agents/                  # 🤖 Orchestration Agent
    │    └── orchestrator/
    │        ├── Dockerfile
    │        ├── README.md
    │        └── orchestrator.py
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



### Application Design Document ###              


[Architecture Design Document](https://github.com/Siri-Gith1/AC215_StockBusters/blob/Milestone4/docs/Architecture_Design_Document_MS4.pdf)


## Solution Architecture ## 

Below is the solution architecture for Stockbusters. For details refer to the design document below

<img width="1095" height="603" alt="image" src="https://github.com/user-attachments/assets/a2b19430-681e-4aa9-947e-65ac0d9d5e79" />
 

## Technical Architecture ##  

The technical architecture for Stockbusters is shown below. For details refer to the design document below

<img width="1094" height="600" alt="image" src="https://github.com/user-attachments/assets/920ed09f-781c-4ced-b5f1-cca1f4b9c4a1" />



### APIs and Frontend Implementation ###  

# API Web Server

The application is built using Python/FastAPI and is configured for containerization via Docker.

It utilizes Google Cloud Storage (GCS) to retrieve three critical data files: Quant model scores, company profiles, and historical stock prices.

Development uses uv for dependency management.

Webserver is deplyed using Uvicorn.

The project maintains code quality and stability via a GitHub Actions CI pipeline that runs linting, unit/integration testing, and coverage checks on every push.

## Tech Stack
 - **FAST API**: API End-points & router functions
 - **Langgraph**: Agents deployment
 - **Langchain**: LLM + RAG retreival
 - **Gemini**: LLM
 - **Uvicorn**: API Web Server
   
# Frontend - Stock Busters

Modern Next.js 15 web application providing an AI-powered conversational interface for personalized stock recommendations and investment analysis.

## Tech Stack

- **Framework**: Next.js 15.5.6 (App Router)
- **Language**: JavaScript/React
- **Styling**: Tailwind CSS + shadcn/ui
- **Charts**: Recharts
- **Authentication**: NextAuth.js


## Features
- **Home Page**: Provides Easy naviagtion to the website
  
  <img width="1272" height="527" alt="image" src="https://github.com/user-attachments/assets/bec01d2b-b21a-47fe-8d87-4dcf6259ebff" />

- **AI Chat Interface**: Conversational AI for investment queries and recommendations
  
  <img width="1261" height="546" alt="image" src="https://github.com/user-attachments/assets/d1cab26c-a071-46d4-b332-7d7a80cb5584" />
  <img width="1945" height="1297" alt="image" src="https://github.com/user-attachments/assets/f255323f-26a2-4569-82bb-d1f5e70e52e7" />

- **Stock Reports**: Sortable tables with Technical/Fundamental/Hybrid AI scores

  <img width="1876" height="843" alt="image" src="https://github.com/user-attachments/assets/77636237-37cd-4faf-953c-2bef3edd9fac" />
  
- **Stock Analysis**: Interactive candlestick charts, volume analysis, and 8 time ranges (1W-MAX)

  <img width="1286" height="1238" alt="image" src="https://github.com/user-attachments/assets/eea7490e-4997-46b0-ae05-4ca85484963c" />

- **User Settings**: Investment profile management (risk tolerance, goals, sectors, time horizon) - In progress

  <img width="1218" height="1307" alt="image" src="https://github.com/user-attachments/assets/cc196c34-3f12-4c69-98e1-92d2e54f93aa" />

- **Theme Support**: Light/Dark mode toggle
  <img width="1254" height="534" alt="image" src="https://github.com/user-attachments/assets/5317509e-af3a-4570-9d09-01c995de4192" />


## Quick Start

1) Run the container by using sh docker-shell.sh command
2) npm install
3) npm install recharts
4) npm run dev
```

Access at: http://localhost:3000

## Configuration

`.env.development`:
```env
NEXT_PUBLIC_BASE_API_URL=http://localhost:9000
NEXTAUTH_SECRET="gHDgDM7d7hcKJWMwqvYzH/6gEZ8gM4Yv5V76Qc/9d/s="
NEXTAUTH_URL=http://localhost:3000
PORT=3000
```

## Development Notes

- Hot reload enabled for instant updates
- Uses App Router for file-based routing
- Session management via X-Session-ID headers
- All API calls through DataService abstraction layer
- Responsive design with Tailwind CSS
- Accessible UI components from shadcn/ui


**Port**: 3000 | **API**: http://localhost:9000 | **Docs**: See [README.md](frontend/README.md) for more details

---

### Continuous Integration and Testing

We have implemented a **Unified CI Pipeline** that automatically builds, tests, and validates all three main components of the Stock Busters application:

- **RAG (Retrieval-Augmented Generation)**: Document processing, embedding, and retrieval
- **Quantamental**: Quantitative analysis and stock prediction models  
- **API-service**: FastAPI-based service for chatbot and stock details

#### Pipeline Features

The unified CI pipeline runs on every push and pull request and includes:

 **Build and Lint**: Automated Docker image builds and code-quality checks (Black, Flake8)  
 **Run Tests**: Executes all test suites (unit, integration, and system tests)  
 **Report Coverage**: Generates and displays unified code coverage reports (minimum 50% combined threshold)  
 **Optimized Execution**: Skips unchanged components to save execution time  
 **Parallel Execution**: Matrix strategy for parallel test runs across components  

#### CI Evidence

**Successful CI Pipeline Execution:**

![Successful Automated Unified CI run on push](docs/Successful%20Automated%20Unified%20CI%20run%20on%20push.png)

*Complete CI pipeline run showing all jobs passing*

**CI Test Summary with Coverage:**

![Unified CI Test Summary](docs/Unified%20CI%20Test%20Summary.png)

*Test summary showing combined coverage (62%) and individual component breakdown*

#### Coverage Results

The pipeline enforces a **minimum 50% combined coverage** threshold across all components. Current coverage:

- **Combined Coverage**: 62% ✅ (exceeds 50% threshold)
- **RAG Component**: 72% line coverage, 66% branch coverage
- **Quantamental Component**: 45% line coverage, 35% branch coverage
- **API-service Component**: 68% line coverage, 63% branch coverage

#### Coverage Reports Location

Coverage reports are automatically generated and committed to the repository:

- **Unified Coverage Report**: `coverage/coverage.xml` (Cobertura format) and `coverage/htmlcov/` (browseable HTML)
- **Component-Specific Reports**:
  - RAG: `src/rag/coverage/coverage.xml` and `src/rag/coverage/htmlcov/`
  - Quantamental: `src/quantamental/coverage/coverage.xml` and `src/quantamental/coverage/htmlcov/`
  - API-service: `src/api-service/coverage/coverage.xml` and `src/api-service/coverage/htmlcov/`

The unified coverage report combines metrics from all components and is updated on every CI run.

#### Documentation

For detailed information about the CI pipeline, including architecture, job descriptions, test types, coverage calculation methodology, and troubleshooting, see:

📖 **[Complete CI Pipeline Documentation](docs/CI_PIPELINE.md)**


##  Quantamental ML Model pipeline

The quantamental pipeline is orchestrated through `main.py`, which executes a 7-step 
workflow:

 - (1) Data collection from the FMP API
 - (2) Feature engineering with 30+ technical and fundamental indicators
 - (3) Model training using Random Forest classification
 - (4) Model validation against quality thresholds (35% minimum, 80% production)
 - (5) Prediction and backtesting with hybrid scoring
 - (6) Optional RAG reasoning via ChromaDB and Vertex AI
 - (7) Data versioning through W&B Artifacts. 

Currently, the pipeline is executed manually via `python main.py`, while GitHub 
Actions handles continuous integration (automated testing and linting on each push). 
All training runs, metrics, and model artifacts are logged to Weights & Biases for 
experiment tracking and reproducibility.

<img width="800" height="765" alt="image" src="https://github.com/user-attachments/assets/11959926-5295-4746-a462-b2c0dcf68b8f" />

### Data and Model Artifact in Weight & Bias ###

<img width="1914" height="897" alt="image" src="https://github.com/user-attachments/assets/d3d0d924-c6eb-4cfe-ae17-65326d934bd2" />

<img width="818" height="513" alt="image" src="https://github.com/user-attachments/assets/7f175574-95a7-4c08-959c-9806dafbf480" />

### Artifact Lineage Tracking & Reproducibility

<img width="1305" height="882" alt="image" src="https://github.com/user-attachments/assets/1b5123c0-78c5-455b-83ec-579b19c3736b" />

The W&B Artifacts Lineage view provides a visual representation of data flow through our ML pipeline, 
enabling full reproducibility and traceability. The graph shows how training runs connect to their 
input and output artifacts.

**What the graph shows:**
- **Training Runs**: `fine-firefly-24` and `giddy-firefly-27` represent pipeline executions
- **Input Artifacts**: `training-data:v1` (processed dataset used for training)
- **Output Artifacts**: `quantamental-model:v3` (trained model), feature importance tables, and run history

**Versioned Artifacts:**
| Type | Artifact | Versions |
|------|----------|----------|
| Raw Data | `input_fundamentals`, `input_sp500_index` | v0, v1 |
| Dataset | `training-data` | v0, v1 |
| Model | `quantamental-model` | v0, v1, v2, v3 |
| Output | `backtest_output`, `output_combined_quantamental` | v0-v3 |

This lineage tracking ensures that any prediction can be traced back through the model, training data, 
and raw inputs—providing complete reproducibility for our ML pipeline.

For example, the run `fine-firefly-24` consumed `training-data:v1` as input and produced `quantamental-model:v3`, feature importance tables, and run history logs as outputs. 
This lineage tracking ensures that for any model version, we can trace back to the exact dataset, hyperparameters, and code that produced it. 

Our versioned artifacts include: raw input data 
(`input_fundamentals`, `input_sp500_index`), processed training data (`training-data`), trained models 
(`quantamental-model` with versions v0-v3), and pipeline outputs (`backtest_output`, `output_combined_quantamental`). 
This comprehensive versioning strategy satisfies the MS4 requirement for data versioning and reproducibility.

### Experiment Tracking & Model Performance

The W&B Workspace provides a comprehensive view of model performance across all training runs. 
The dashboard displays key metrics including ROC-AUC, precision, recall, and probability 
distributions for each experiment. The confusion matrices compare predictions between runs 
(e.g., `giddy-firefly-27` vs `fine-firefly-24`), showing the model correctly identifies 
approximately 125 true negatives and 52 true positives, with 71 false positives and 165 
false negatives. This visualization enables quick comparison across 27 tracked runs, helping 
identify which configurations produce the best results and supporting iterative model improvement.

<img width="1840" height="791" alt="image" src="https://github.com/user-attachments/assets/88bc93a2-4e57-4fea-a465-53a4a39d80f2" />

<img width="841" height="420" alt="image" src="https://github.com/user-attachments/assets/accfbf78-a1ad-4a8b-a414-9f90148c028c" />

<img width="897" height="746" alt="image" src="https://github.com/user-attachments/assets/9f71f04d-9e1d-448f-b9d3-f83061786d14" />







## Data Versioning Implementation

Our pipeline implements data versioning at multiple levels to ensure full reproducibility:

### W&B Artifacts (Primary Versioning)

Weights & Biases Artifacts serves as our primary data versioning system, tracking all datasets 
and models with automatic version increments:

| Artifact Type | Name | Description | Versions |
|---------------|------|-------------|----------|
| **Raw Data** | `input_fundamentals` | Quarterly financial metrics from FMP API | v0, v1 |
| **Raw Data** | `input_sp500_index` | S&P 500 index prices | v0, v1 |
| **Dataset** | `training-data` | Processed features for model training | v0, v1 |
| **Model** | `quantamental-model` | Trained Random Forest classifier | v0, v1, v2, v3 |
| **Output** | `backtest_output` | Prediction results with rankings | v0, v1, v2, v3 |

Each artifact version includes:
- **Metadata**: Accuracy, validation status, training date
- **Lineage**: Links to the run that created it
- **Files**: Actual data files (parquet, pkl, csv)

<img width="1024" height="656" alt="image" src="https://github.com/user-attachments/assets/8f8739b1-a103-4fa3-be6a-45ee3de7a713" />


### GCS Bucket (Timestamped Outputs)

Pipeline outputs are also stored in Google Cloud Storage with timestamps for additional versioning:
```
gs://fin-data-bucket-115/model_output/
├── combined_quantamental_20241120_143558.csv
├── combined_quantamental_20241124_173024.csv
└── backtest_results_20241125_162002.csv
```
Example from GCS bucket
<img width="1198" height="931" alt="image" src="https://github.com/user-attachments/assets/3db6f2e8-56d7-468e-ae42-5e71108e7ebb" />



The timestamp format `YYYYMMDD_HHMMSS` allows chronological tracking of all pipeline runs.

### Version Metadata Files

Each pipeline run generates a version info file (`version_info_ms4.json`) containing:
```json
{
  "timestamp": "2024-11-25T16:20:02",
  "model_version": "v3",
  "accuracy": 0.39,
  "validation_status": "degraded",
  "data_version": "training-data:v1",
  "git_commit": "abc123..."
}
```

### Why This Approach?

We chose W&B Artifacts over DVC because:
1. **Unified Platform**: Experiment tracking and versioning in one place
2. **Automatic Lineage**: Visual graph connecting data → runs → models
3. **Metadata Support**: Store accuracy, status alongside artifacts
4. **No Extra Infrastructure**: Built-in cloud storage (vs. DVC requiring remote setup)



## Model Evaluation ## 
    Should include:
    Training scripts/config files, dataset references (versioned), and experiment logs.
    A concise summary of key results and how the fine-tuned model affects your deployment strategy.

    Data Versioning documentation (methodology, justification, and usage instructions)
    Model Training/Fine-Tuning summary (training process, results, and deployment implications)
