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
    │   ├── Dockerfile
    │   ├── README.md
    │   ├── package.json
    │   └── components.json
    │
    └── 📁 agents/                  # 🤖 Orchestration Agent
    │    └── orchestrator/
    │        ├── Dockerfile
    │        ├── README.md
    │        └── orchestrator.py
    ├── secrets/
    └── service-account.json          ← for GCS
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



### Application Design Document ###              (Mahmood/Majid/Seraphim)

## Solution Architecture ## (Mahmood/Majid/Seraphim)
  ** from MS4 requirement, please add   High-level overview of system components and their interactions (e.g., data flow, APIs, frontend, model). >  <-- delete this line once completed **

## Technical Architecture ##  (Mahmood/Majid/Seraphim)

<from MS4 requirement please add Technologies, frameworks, and design patterns used, and how they support your overall system design.> <-- delete this line once completed

### APIs and Frontend Implementation ###  (Mahmood/Majid)

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

** Below is from MS3 **
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
