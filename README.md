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

## please review your own section. it is mocked up structure - Seraphim /Majid/Mahmood/Siri ##

```
AC215_StockBusters/
│
├── src/
│   ├── quant-pipeline/              ← Data pipeline, quantamental model, hybrid score calculation , backtest
│   │   ├── data_fetch.py
│   │   ├── data_preprocess.py
│   │   ├── feature_engineering.py
│   │   ├── model_train.py
│   │   ├── hybrid_score.py
│   │   ├── backtest.py
│   │   ├── export_outputs.py
│   │   ├── config.py
│   │   └── run_pipeline.py          
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
│   ├── frontend/
│   │   ├── app/
│   │   │   ├── chat/              # Chat interface
│   │   │   ├── report/            # Stock reports
│   │   │   ├── stock-detail/      # Stock detail pages
│   │   │   ├── settings/          # User settings
│   │   │   ├── page               # Home page
│   │   │   └── layout             # Header, Footer, Theme
│   │   │
│   │   ├── components             # components for corresponding app pages plus share ui component
│   │   ├── lib/
│   │   │   ├── DataService.js     # API integration
│   │   │   ├── Common.js
│   │   │   └── utils.js
│   │   └── .env.development
│   │
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

  
- **Stock Analysis**: Interactive candlestick charts, volume analysis, and 8 time ranges (1W-MAX)
- **User Settings**: Investment profile management (risk tolerance, goals, sectors, time horizon) - In progress
- **Theme Support**: Light/Dark mode toggle

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

---

**Port**: 3000 | **API**: http://localhost:9000 | **Docs**: See [README.md](frontend/README.md) for more details


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

## Front End CI Pipeline & Evidence ## (Mahmood)--- Not needed for Front end, please remove this section.
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
