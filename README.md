## AC215/CSCIE-115 - Milestone 5: An Agentic System for Stock Recommendations

**Team Members** : Majid Uppal, Sirisom Pranivong, Seraphim Eilken, Mahmood Masqati

**Group Name**  Stock Busters

**Overview**

Stock Busters Application empowers everyday investors who are overwhelmed by information overload and analysis paralysis. Our AI-powered agent delivers personalized stock recommendations with clear reasoning, replacing static dashboards with conversational intelligence that adapts to each user's goals and risk tolerance.
The system combines fundamental analysis (company financials) with technical analysis (market indicators) to predict which S&P 500 stocks are likely to outperform the market. Through an interactive chatbot, users receive tailored Buy/Hold/Avoid signals with AI-generated explanations—making professional-grade investment insights accessible to novice investors, busy professionals, and DIY retirement savers alike.

**What is new in MS5?**


Milestone 5 transforms our project from a **locally functional system** (MS4) to a **production-grade deployed application**.





### MS4 → MS5 Progression

| Category | MS4 | MS5 |
|----------|-----|-----|
| **ML Deployment** | Local/Container | Cloud Run Jobs + Cloud Scheduler |
| **Application Hosting** | Local development | Google Kubernetes Engine (GKE) |
| **Infrastructure** | Manual setup | Pulumi IaC |
| **CI/CD** | Testing only (51%) | Full CI/CD + Deploy (62%) |
| **Accessibility** | Local only | Public URL |

### New Components Added

| Component |  Description |
|-----------|-------------|
| Cloud Run Deployment | ML pipeline on serverless infrastructure |
| Cloud Scheduler | Automated daily retraining (6 AM CT) |
| Kubernetes Deployment | GKE cluster for application |
| Pulumi Infrastructure | Infrastructure as Code |
| CD Pipeline | Auto-deploy to Kubernetes |

---

## Application Screenshots

*Welcome screen with stock recommendations*
<img width="1254" height="534" alt="image" src="https://github.com/user-attachments/assets/5317509e-af3a-4570-9d09-01c995de4192" />


*Individual stock analysis with price charts*
  <img width="1286" height="1238" alt="image" src="https://github.com/user-attachments/assets/eea7490e-4997-46b0-ae05-4ca85484963c" />
---

# Technical Implementation

### Application Design Document ###              


[Architecture Design Document](https://github.com/Siri-Gith1/AC215_StockBusters/blob/Milestone4/docs/Architecture_Design_Document_MS4.pdf)


## Solution Architecture ## 

Below is the solution architecture for Stockbusters. For details refer to the design document below

<img width="1884" height="1036" alt="image" src="https://github.com/user-attachments/assets/d5731820-21c6-4cd8-8e4f-7e1c26f64e70" />

# 📈 StockBusters: An Advanced AI-Driven Personalized Stock Recommendation System

## Introduction

The financial market is complex and constantly evolving, making personalized, data-driven investment advice invaluable. **StockBusters** is a sophisticated stock recommendation system designed to provide tailored investment insights by harmoniously blending **user personalization, deep financial data analysis, machine learning intelligence, and advanced LLM-based reasoning.**

This document outlines the core architectural components that drive the system.

## 🧠 Architectural Components

The system is built on six interconnected modules that handle everything from user input to final report generation.

### 1. The Personalization Engine: User Preference Collection Bot 🤖

This module serves as the primary user interface for gathering tailored investment parameters.

* **Function:** Gathers critical user inputs, including **risk tolerance, investment horizon, and personalized investment criteria**.
* **Key Capability:** Capable of answering clarifying questions to ensure accurate capture of financial choices.
* **Output:** Feeds the validated user profile directly into the **Stock Recommender**.

### 2. The Foundation: Finance Data Pipeline 📊

The core data ingestion and processing engine, ensuring high-quality data for analysis.

* **Function:** Sourcing, cleaning, and processing raw financial data (e.g., **historical prices, company fundamentals, and sector information**).
* **Core Task:** Transforms raw, messy data into a structured format ready for model consumption.
* **Output:** Clean, structured data input for the **ML Models**.

### 3. The Intelligence Core: ML Models (Machine Learning) 🔬

The quantitative analysis layer responsible for objective stock evaluation.

* **Input Data:**
    * **Fundamental:** Metrics like ROE, ROIC, FCF Yield, Debt to Equity, cash, and revenue.
    * **Technical:** Opening/closing prices, volume, daily high/low.
* **Process:** Computes intermediate metrics and performs comprehensive analysis to generate objective decisions and **stock rankings** based on both fundamental and technical health.

### 4. The Reasoning and Context: LLM with RAG (Retrieval-Augmented Generation) 📚

This module provides the "why" behind the recommendation, acting as an expert advisor.

* **Function:** Combines the quantitative output of the ML Model with **expert financial knowledge** retrieved via the RAG system.
* **Role:** Generates **robust, enriched reasoning and context** to explain *why* a particular stock was selected.
* **Output:** Passes the contextualized rationale to the **Stock Recommender**.

### 5. The Synthesis and Decision-Making: Stock Recommender 🎯

The central decision-making unit that synthesizes all intelligence into a final, actionable plan.

* **Synthesis:** Integrates three critical inputs:
    1.  **User Preferences** (from the Bot)
    2.  **Model Output** (from the ML Models)
    3.  **LLM Context** (from the Reasoning Engine)
* **Result:** Produces the final, **tailored personalized recommendations** that align with the user's financial profile.

### 6. The User Experience: Recommendation and Reporting 📝

The final stage, focused on transparent delivery of insights.

#### A. Stocks Report
* **Description:** The primary personalized output delivered to the user.
* **Content:** Summarizes the recommendations, including **Key Performance Indicators (KPIs)** and an initial **risk assessment**.

#### B. Stock Details
* **Description:** A drill-down component for granular stock information.
* **Content:** Provides in-depth company details, stock trend analysis, and the **full rationale** for the recommendation, enlightening users on the decision-making process.
 

## Technical Architecture ##  

The technical architecture for Stockbusters is shown below. For details refer to the design document below

<img width="1853" height="1062" alt="image" src="https://github.com/user-attachments/assets/4a41fcf6-7f29-403d-86c2-382b96949920" />


# ⚙️ Technical Architecture of StockBusters

The **StockBusters** recommendation system is built upon a robust, layered technical architecture designed to support application development, advanced AI/ML capabilities, and a seamless conversational interface powered by Large Language Models (LLMs) like Gemini.

The architecture is logically separated into three distinct and interconnected layers: **Process**, **Execution**, and **State**. 

---

## 1. The Process Layer: User and High-Level Functionality 🚀

This is the top-most layer, defining the primary functional areas and points of interaction supported by the system.

* **Develop App:** Standard activities related to application development, ensuring integration with the lower layers.
* **AI/ML Tasks:** Focuses on core intelligent functions, including all aspects of **model development and training**.
* **Chat Bot:** The crucial conversational interface that enables **Human Interactions** to efficiently collect detailed financial preferences for personalized recommendations.

---

## 2. The Execution Layer: Runtime Components and Logic ⚙️

This layer contains the runtime components, services, and core logic that handle processing, application behavior, and user interaction.

| Component | Function | Key Role |
| :--- | :--- | :--- |
| **Frontend (StockBusters)** | The user-facing application interface. | Supports **Human Interactions** and communicates with the Backend via HTTP/HTTPS. |
| **Backend** | Core application logic and data-handling services. | Accessible via HTTPS; manages primary system functions and data flow. |
| **API Service** | Handles core business logic. | Serves data and processing logic to the **Frontend** and **LLMs**. |
| **LLMs (as a Service)** | Utilizes **Gemini** with **RAG** (Retrieval-Augmented Generation) support. | Uses the financial knowledge base to generate detailed **reasoning for stock selections**. |
| **Agents Layer** | A network of cooperative agents. | Collects user preferences and converts natural language input into **structured data objects** for the ML model. |
| **Interactive Notebooks** | Development environment for data scientists/developers. | Facilitates experimentation, development, and connects to the LLMs and the State Layer. |

### The Automated ML Pipeline 🔗

A critical workflow within the Execution Layer that manages the end-to-end machine learning lifecycle:

* **Data Collector:** Gathers raw financial data through **API calls** from external datasources.
* **Data Processor:** Prepares the data for training or inference, including **preprocessing and cleanup**.
* **Model Training:** The AI/ML model is trained using the cleansed and processed data.
* **Model Deploy:** The trained model is deployed into a **production environment** for real-time inference and use.

---

## 3. The State Layer: Data, Storage, and Infrastructure 💾

The foundational layer responsible for storing, managing, and tracking all persistent assets and data required for the system's operation.

* **Data Store:** Persistent storage for all **raw, processed, and training data** used by the ML Pipeline and LLMs.
* **Knowledge Base:** Stores proprietary finance knowledge, implemented in a **Vector DB (e.g., Chroma DB)**, crucial for the LLM's reasoning capabilities.
    * **Vector DB Service:** The operational service that manages and provides the vector database for the LLM's financial knowledge base.
* **Source Control:** Stores all application code, configuration files, and definitions (including pipeline configurations).
* **Artifact Registry:** Repository for built artifacts, most importantly the **trained models** generated by the ML Pipeline.

---
## 1.## 🚀 Deployment

Stock Busters is deployed on **Google Kubernetes Engine (GKE)** using **Pulumi** for infrastructure-as-code.

<img width="2119" height="227" alt="image" src="https://github.com/user-attachments/assets/0675e3dd-75eb-460e-8c80-f5eff1b27b99" />

### Architecture

- **Frontend**: Next.js application
- **API Service**: FastAPI backend with AI-powered stock analysis
- **Infrastructure**: GKE cluster with NGINX Ingress and Workload Identity
- **Cloud Services**: Google Cloud Storage, Vertex AI, Artifact Registry

### Quick Deployment

#### Prerequisites
- Docker Desktop
- Google Cloud SDK
- GCP project with billing enabled
- Service account with appropriate IAM roles

#### Deploy in 3 Steps

**1. Setup Deployment Container**
```bash
cd src/deployment
sh docker-shell.sh
```

**2. Build and Push Images (~15-20 min)**
```bash
cd /app/deploy_images
pulumi stack select dev
pulumi up
```

**3. Deploy to Kubernetes (~20-25 min)**
```bash
cd /app/deploy_k8s
pulumi stack select dev
pulumi up
```

**Access your application:**
```bash
pulumi stack output app_url
# Example: http://34.60.47.248.sslip.io
```

### Deployment Features

✅ **Autoscaling**: 1-3 nodes based on demand  
✅ **Zero-downtime updates**: Rolling deployments  
✅ **Secure authentication**: Workload Identity (no embedded keys)  
✅ **Load balancing**: NGINX Ingress Controller  
✅ **Infrastructure as Code**: Declarative Pulumi configuration  

### Quick Commands
```bash
# Check deployment status
kubectl get pods -n stockbusters-app-namespace

# View logs
kubectl logs -f deployment/api -n stockbusters-app-namespace

# Update application
kubectl rollout restart deployment/api -n stockbusters-app-namespace

# Cleanup
cd /app/deploy_k8s && pulumi destroy
```

### Cost Estimate
- **Monthly**: ~$116-166 (GKE cluster, nodes, load balancer)
- **Optimization**: Use preemptible nodes, smaller machine types, or GKE Autopilot

### Detailed Documentation

For complete deployment instructions, troubleshooting, and configuration details, see [src/deployment/README.md](src/deployment/README.md)

**Live Demo:** http://34.60.47.248.sslip.io

### Demonstrating Scalability and Load Balancing

One of the key advantages of Kubernetes is its ability to scale applications seamlessly. We conducted live tests to demonstrate both horizontal pod scaling and load balancing capabilities.

### Initial State

Before scaling, our application ran with minimal resources:
```
NAME                      READY   STATUS    RESTARTS   AGE
api-5b876fcbb8-kdcfm      1/1     Running   0          46m
frontend-6d98787d89-mxhks 1/1     Running   0          47m
```

**Resource Usage:**
- Node CPU: 4%
- Node Memory: 54%
- 1 API pod, 1 Frontend pod

### Scaling Operation

Using a single kubectl command, we scaled both services to 3 replicas:
```bash
kubectl scale deployment/api --replicas=3 -n stockbusters-app-namespace
kubectl scale deployment/frontend --replicas=3 -n stockbusters-app-namespace
```

Within 60 seconds, all new pods were running and ready to serve traffic:
```
NAME                          READY   STATUS    RESTARTS   AGE
api-5b876fcbb8-55djf          1/1     Running   0          61s
api-5b876fcbb8-648wr          1/1     Running   0          61s
api-5b876fcbb8-kdcfm          1/1     Running   0          48m
frontend-6d98787d89-65gjq     1/1     Running   0          60s
frontend-6d98787d89-dljc5     1/1     Running   0          60s
frontend-6d98787d89-mxhks     1/1     Running   0          48m
```

**Key observation:** Zero downtime during the scaling operation. The original pods continued serving traffic while new pods were provisioned.

### Load Testing Results

We used Apache Bench to simulate real-world traffic with 1,000 requests and 50 concurrent connections:
```bash
ab -n 1000 -c 50 http://34.60.47.248.sslip.io/
```

**Results:**

| Metric | Value |
|--------|-------|
| Requests per second | **136.18 req/sec** |
| Mean response time | 367 ms |
| Failed requests | **0 (100% success)** |
| Total test duration | 7.3 seconds |

**Response Time Distribution:**
- 50% of requests: < 335ms
- 90% of requests: < 445ms
- 99% of requests: < 593ms

### Load Balancing in Action

Our NGINX Ingress Controller automatically distributed traffic across all 6 application pods:
```
Service Architecture:
┌─────────────────────────────────────┐
│   Load Balancer (34.60.47.248)     │
└──────────────┬──────────────────────┘
               │
       ┌───────▼────────┐
       │ NGINX Ingress  │
       └───────┬────────┘
               │
       ┌───────┴────────┐
       │                │
   ┌───▼───┐        ┌───▼───┐
   │  API  │        │Frontend│
   │ (x3)  │        │  (x3)  │
   └───────┘        └────────┘
```

**Evidence of Load Distribution:**

After scaling, we observed CPU usage spread across all pods:
```
NAME                      CPU(cores)   MEMORY(bytes)
api-5b876fcbb8-55djf      796m         546Mi
api-5b876fcbb8-648wr      595m         538Mi
api-5b876fcbb8-kdcfm      2m           551Mi
```

The varying CPU usage across pods confirms that the load balancer is distributing requests to different backend instances.

### Scaling Comparison

| Aspect | Before (1 replica) | After (3 replicas) |
|--------|-------------------|-------------------|
| Total Pods | 2 | 6 (3x) |
| API Pods | 1 | 3 |
| Frontend Pods | 1 | 3 |
| Request Success Rate | 100% | 100% |
| Failed Requests | 0 | 0 |
| Node CPU Usage | 4% | 4% |
| Scaling Time | - | ~60 seconds |
| Downtime | - | 0 seconds |

### Key Takeaways

1. **Instant Scalability**: Scaled from 1 to 3 replicas in under 60 seconds
2. **Zero Downtime**: No service interruption during scaling
3. **Perfect Reliability**: 0% failure rate under load
4. **Efficient Load Distribution**: Traffic automatically balanced across all pods
5. **Resource Efficient**: Even after 3x scaling, node CPU remained at 4%

For more details please check [src/deployment/scaling_demo_output.txt](src/deployment/scaling_demo_output.txt) , [src/deployment/Scaling_Proof.md](src/deployment/Scaling_Proof.md) , [src/deployment/quick_scaling_demo.sh](src/deployment/quick_scaling_demo.sh)

---

## 3. CI/CD Pipeline (GitHub Actions)

> **Requirement**: Set up a CI/CD pipeline that includes unit tests for each service, integration tests, auto-deploy on merge to main, 60%+ coverage, and documentation of untested functions.

We have implemented a **Unified CI Pipeline** that automatically builds, tests, and validates all three main components of the Stock Busters application:

- **RAG (Retrieval-Augmented Generation)**: Document processing, embedding, and retrieval
- **Quantamental**: Quantitative analysis and stock prediction models  
- **API-service**: FastAPI-based service for chatbot and stock details

### ✅ Requirements Checklist

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Unit test suite for each service/container | ✅ | [See Test Structure](#test-structure) |
| Integration tests on codebase | ✅ | [See Test Types](#test-types) |
| Deploy on merge to `main` | ✅ | [See Deployment Pipeline](#deployment-pipeline) |
| 60%+ line coverage | ✅ **70%** | [See Coverage Results](#coverage-results) |
| Document untested functions | ✅ | [See Untested Functions](#untested-functions) |

### Pipeline Architecture

The CI/CD pipeline consists of two main workflows:

**CI Pipeline (`.github/workflows/ci.yml`):**
```
┌─────────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────────┐
│ detect-changes  │───▶│    build    │───▶│    tests    │───▶│ test-summary │
│                 │    │  (matrix)   │    │  (matrix)   │    │              │
└─────────────────┘    └─────────────┘    └─────────────┘    └──────────────┘
        │                    │                  │                    │
   Identifies           Builds Docker      Runs lint,          Combines
   changed              images for         unit, integration,  coverage
   components           each component     system tests        reports
```

**CD Pipeline (`.github/workflows/cd.yml`):**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ CI Completes    │───▶│ Build Images to  │───▶│ Deploy to K8s   │
│ Successfully    │    │ Artifact Registry │    │ via Pulumi      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Workflow Triggers

**CI Pipeline Triggers:**
- **Push events** to `main`, `develop`, or `Milestone5` branches (when code in `src/rag/`, `src/quantamental/`, or `src/api-service/` changes)
- **Pull requests** to `main`, `develop`, or `Milestone5` branches
- **Manual dispatch** via GitHub Actions UI

**CD Pipeline Triggers:**
- **Workflow run completion**: Automatically triggers when CI pipeline completes successfully on `main`, `develop`, or `Milestone5` branches
- **Push events** to `main`, `develop`, or `Milestone5` branches (when `.github/workflows/cd.yml`, `src/deployment/**`, or `src/frontend/**` changes)
- **Manual dispatch** via GitHub Actions UI

**Optimization:** The CI pipeline uses path-based change detection to skip building and testing unchanged components, reducing execution time.

### Pipeline Features

The unified CI pipeline runs on every push and pull request and includes:

- **Build and Lint**: Automated Docker image builds and code-quality checks (Black, Flake8)  
- **Run Tests**: Executes all test suites (unit, integration, and system tests)  
- **Report Coverage**: Generates and displays unified code coverage reports (minimum 50% combined threshold)  
- **Optimized Execution**: Skips unchanged components to save execution time  
- **Parallel Execution**: Matrix strategy for parallel test runs across components  

### CI Evidence

**Successful CI Pipeline Execution:**

![Successful Automated Unified CI run on push](docs/Successful%20Automated%20Unified%20CI%20run%20on%20push.png)

*Complete CI pipeline run showing all jobs passing*

**CI Test Summary with Coverage:**

![Unified CI Test Summary](docs/Unified%20CI%20Test%20Summary.png)

*Test summary showing combined coverage (70%) and individual component breakdown*

### Test Structure

Each service has its own comprehensive test suite:

```
src/
├── rag/tests/
│   ├── unit/                    # 151 unit tests
│   │   ├── test_rag_core.py
│   │   ├── test_rag_internals.py
│   │   ├── test_retriever.py
│   │   ├── test_gcs_sync.py
│   │   ├── test_ingestion.py
│   │   ├── test_pdf_processing.py
│   │   └── test_utilities.py
│   ├── integration/             # 15 integration tests
│   │   ├── test_rag_api.py
│   │   └── test_rag_e2e.py
│   └── system/                  # 8 system tests
│       └── test_rag_system.py
│
├── quantamental/tests/
│   ├── test_unit_utils.py       # 60+ unit tests
│   ├── test_unit_data_collect.py
│   ├── test_unit_data_process.py
│   ├── test_integration_modules.py  # 30+ integration tests
│   ├── test_integration_pipeline.py
│   └── test_system_pipeline.py  # 5-10 system tests
│
└── api-service/tests/
    ├── test_unit_routers.py     # Unit tests for API router endpoints (25 tests)
    ├── test_chat_bot_agent.py   # Unit tests for ChatAgent and models (17 tests)
    ├── test_detailed_page_funcs.py  # Unit tests for stock detail utilities (27 tests)
    ├── test_service.py          # Unit tests for main FastAPI service (9 tests)
    ├── test_gcs_bucket.py       # Unit tests for GCS bucket operations (8 tests)
    ├── test_integration_api.py  # Integration tests for API endpoints (27 tests)
    ├── test_system_api.py       # System tests for live container (16 tests)
    └── conftest.py              # Pytest fixtures and shared test utilities
```

**Total Test Count:**
- **RAG Component**: 174 tests (151 unit + 15 integration + 8 system)
- **Quantamental Component**: 90+ tests (60+ unit + 30+ integration + 5-10 system)
- **API-service Component**: 130+ tests (86 unit + 27 integration + 16 system)
- **Total**: 390+ tests across all components

### Test Types

| Type | Marker | Purpose | Runs On | Coverage |
|------|--------|---------|---------|----------|
| **Unit** | `@pytest.mark.unit` | Test individual functions in isolation | All branches | Collected |
| **Integration** | `@pytest.mark.integration` | Test component interactions with mocked services | All branches | Collected |
| **System** | `@pytest.mark.system` | End-to-end tests with running services | `main`, `develop`, `Milestone5` | Not collected |
| **Lint** | N/A | Code quality checks (Black, Flake8) | All branches | N/A |

**Test Execution:**
- Tests run in parallel using matrix strategy (one job per component per test type)
- System tests require Docker containers and are slower (~10-30 seconds)
- Unit and integration tests are fast (< 5 seconds each)
- Coverage is collected for unit and integration tests only

### Coverage Results

The pipeline enforces a **minimum 50% combined coverage** threshold across all components.

**📈 Combined Coverage Report**

- **Combined Coverage**: 70% ✅ (meets 50% threshold, exceeds 60% requirement)

**Component Breakdown**

- 🔍 **RAG Component**
  - Coverage: 73%
  - Branch Coverage: 67%

- 📊 **Quantamental Component**
  - Coverage: 62%
  - Branch Coverage: 46%

- 🚀 **API-service Component**
  - Coverage: 78%
  - Branch Coverage: 67%

**Test Status**: 🎉 All tests passed!

**Coverage Calculation:**
- Combined coverage is a **weighted average** based on total lines: `(Total Lines Covered / Total Lines Valid) × 100`
- Individual component coverage files are merged into a unified report: `coverage/coverage.xml`
- Coverage reports are automatically committed to the repository after each CI run

**Coverage Reports Location:**

Coverage reports are automatically generated and committed to the repository:

- **Unified Report**: `coverage/coverage.xml` (Cobertura format) and `coverage/htmlcov/` (HTML)
- **Component-Specific**: 
  - RAG: `src/rag/coverage/coverage.xml` and `src/rag/coverage/htmlcov/`
  - Quantamental: `src/quantamental/coverage/coverage.xml` and `src/quantamental/coverage/htmlcov/`
  - API-service: `src/api-service/coverage/coverage.xml` and `src/api-service/coverage/htmlcov/`

The unified coverage report combines metrics from all components and is updated on every CI run.

### Documentation

For detailed information about the CI pipeline, including architecture, job descriptions, test types, coverage calculation methodology, and troubleshooting, see:

📖 **[Complete CI Pipeline Documentation](docs/CI_PIPELINE.md)**

### Deployment Pipeline

The CD pipeline automatically deploys to Kubernetes when CI completes successfully. For complete documentation, see:

📖 **[CD Pipeline Documentation](docs/CD_PIPELINE.md)**

![Successful Automatic CD run after CI run](docs/Successful%20Automatic%20CD%20run%20after%20CI%20run.png)

*CD pipeline automatically triggered after successful CI pipeline completion*

**Quick Overview:**
- **Trigger**: CI pipeline completes successfully on `main`, `develop`, or `Milestone5` branch
- **Authentication**: Uses Workload Identity Federation (OIDC) for secure GCP access (no secrets required)
- **Build Images**: Builds Docker images and pushes to GCP Artifact Registry
- **Deploy Infrastructure**: Uses Pulumi to deploy/update Kubernetes cluster
- **Verification**: Waits for pods to be ready and verifies application health
- **Execution Time**: 7-8 minutes (optimized for faster deployment)

### Untested Functions

> **Required**: Document which functions and modules are not covered by tests.

All untested functions are documented with justifications:

**RAG Component:**
- **Location**: `src/rag/docs/UNTESTED_FUNCTIONS.md`
- **Untested Functions**: 2 functions
  - `get_retriever()`: Singleton factory (trivial logic, tested via integration)
  - `make_app()`: FastAPI app creation (tested via integration tests with HTTP requests)
- **Justification**: Both functions are tested indirectly through integration tests. Direct unit tests would require extensive mocking that duplicates integration coverage.

**API-service Component:**
- **Location**: `src/api-service/docs/UNTESTED_FUNCTIONS.md`
- **Untested Functions**: 
  - API validation error paths (most tested in integration tests)
  - Module-level initialization code (credential loading)
  - Edge cases in error handling
- **Justification**: Most validation errors are tested in integration tests. Critical business logic and API endpoints are fully covered.

**Quantamental Component:**
- **Location**: `src/quantamental/docs/UNTESTED_FUNCTIONS.md` (referenced in README)
- **Coverage**: Lower coverage in `backtest.py` (11%) and `model_train.py` (17%)
- **Justification**: Core data processing and feature engineering are well-tested. Model training and backtesting are validated through system tests.

**Summary**: All untested functions are documented with clear justifications. Critical business logic, API endpoints, and core functionality are fully tested. The 70% combined coverage significantly exceeds the 60% minimum requirement.

---
## 4. Machine Learning Workflow  

> **Requirement**: Demonstrate a production-ready ML workflow including data preprocessing, training, evaluation, automated retraining, and validation checks.

### Overview

The Quantamental ML workflow has been deployed to **Google Cloud Run Jobs**, a serverless compute platform that enables scalable execution without infrastructure management. Automated daily retraining is orchestrated through **Google Cloud Scheduler**, configured to trigger pipeline execution at 6 AM Central Time to capture the latest market data before trading hours.

### Why Cloud Run Jobs + Cloud Scheduler?

Cloud Run Jobs and Cloud Scheduler were selected over Kubernetes-based solutions for the ML pipeline for several strategic reasons:

| Reason | Benefit |
|--------|---------|
| **Pay-per-execution** | Pipeline only incurs costs during ~15-30 min daily execution, not 24/7 infrastructure |
| **Operational simplicity** | No Kubernetes CronJobs, pod scheduling, or resource tuning for batch workloads |
| **Automatic scaling** | CPU and memory provisioned on-demand without manual intervention |
| **Native GCP integration** | Unified authentication, monitoring, and logging through single console |

### Requirements Checklist

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Data preprocessing integrated | ✅ | [Steps 1-2](#pipeline-steps) |
| Model training integrated | ✅ | [Step 3](#pipeline-steps) |
| Evaluation integrated | ✅ | [Step 4](#pipeline-steps) |
| Automated retraining on new data/code | ✅ | [Cloud Scheduler](#automated-retraining) |
| Validation checks (performance thresholds) | ✅ | [Validation Framework](#validation-framework) |

> **Architecture Pattern**: Kubernetes handles the user-facing application (high availability), while Cloud Run handles periodic batch ML workloads (cost-optimized). This separation of concerns optimizes both cost and operational overhead.

### 7-Step Pipeline Workflow

| Step | Module | Description |
|------|--------|-------------|
| 1 | `data_collect.py` | Fetch data from FMP API ( S&P 500 stocks) |
| 2 | `data_process.py` | Feature engineering (30+ technical & fundamental indicators) |
| 3 | `model_train.py` | Random Forest training with hyperparameter configuration |
| 4 | `model_validation.py` | Validate against quality thresholds |
| 5 | `backtest.py` | Generate predictions with hybrid scoring (Buy/Hold/Avoid) |
| 6 | `generate_stock_reasoning.py` | RAG-powered reasoning via Vertex AI (optional) |
| 7 | `data_versioning.py` | Version artifacts to W&B for reproducibility |

### Feature Engineering

**Technical Indicators (8 features):**

| Feature | Description |
|---------|-------------|
| `return_1m` | 1-month price return |
| `ema_12`, `ema_26` | Exponential moving averages |
| `macd`, `macd_signal`, `macd_hist` | MACD indicators |
| `RSI_14` | Relative Strength Index |
| `volatility_21d` | 21-day volatility |

**Fundamental Indicators (22+ features):**

| Category | Features |
|----------|----------|
| Profitability | `roe`, `roic`, `netProfitMargin`, `earningsYield` |
| Valuation | `peRatio`, `pbRatio`, `evToEbitda`, `freeCashFlowYield` |
| Leverage | `debtToEquity`, `netDebtToEBITDA`, `interestCoverage` |
| Liquidity | `currentRatio`, `quickRatio`, `cashRatio` |
| Growth | `revenueGrowth`, `earningsGrowth`, `dividendYield` |

### Security & Infrastructure

| Component | Service | Purpose |
|-----------|---------|---------|
| **Secrets** | Google Secret Manager | Secure storage for FMP & W&B API keys |
| **Container Images** | Google Artifact Registry | Version-controlled Docker images |
| **Model Outputs** | Google Cloud Storage | Timestamped predictions & data files |
| **Experiment Tracking** | Weights & Biases | Metrics, artifacts, and lineage tracking |

### Automated Retraining

**Trigger: Cloud Scheduler**

| Parameter | Value |
|-----------|-------|
| **Schedule** | `0 6 * * *` (Daily at 6 AM Central) |
| **Timezone** | America/Chicago |
| **Trigger Type** | HTTP POST to Cloud Run Job |

**Retraining Flow:**

```
Cloud Scheduler (6 AM CT)
        │
        ▼
Cloud Run Job executes main.py
        │
        ├──▶ Fetches latest market data (FMP API)
        ├──▶ Recomputes features
        ├──▶ Retrains model
        ├──▶ Validates performance
        ├──▶ Generates predictions
        └──▶ Versions artifacts (W&B)
```

### Validation Framework

The validation framework implements a three-tier classification system:

| Status | Threshold | Action |
|--------|-----------|--------|
| 🟢 **Production** | ≥ 80% accuracy | Full deployment |
| 🟡 **Degraded** | 35% - 79% accuracy | Deploy with monitoring |
| 🔴 **Rejected** | < 35% accuracy | Block deployment |

This automated quality gate ensures deployment reliability while maintaining transparency about model performance limitations.

**Current Model Performance:**

| Metric | Value | Status |
|--------|-------|--------|
| **Accuracy** | 43.62% | 🟡 Degraded |
| **Precision** | 44.60% | Below target |
| **Recall** | 27.19% | Below target |
| **F1-Score** | 33.79% | Below target |
| **ROC-AUC** | 40.29% | Moderate |

**Why 35% Minimum Threshold?**

1. **Stock prediction is inherently difficult** - even professionals struggle to beat the market
2. **Above random chance** - 35% exceeds random 3-class prediction (33%)
3. **Probability scores add value** - rankings work even with moderate accuracy
4. **Framework demonstration** - shows validation system works correctly
5. **Transparency** - honest about limitations rather than hiding them

### Data Versioning

**W&B Artifacts:**

| Artifact | Type | Versions |
|----------|------|----------|
| `input_fundamentals` | Dataset | v0-v1 |
| `training-data` | Dataset | v0-v1 |
| `quantamental-model` | Model | v0-v3 |
| `backtest_output` | Results | v0-v3 |

**Lineage Tracking:**

```
[training-data:v1] ──▶ [Run: giddy-firefly-27] ──▶ [quantamental-model:v3]
                                │
                                └──▶ [backtest_output:v3]
```

### Deployment Configuration

| Parameter | Value |
|-----------|-------|
| **Image** | `us-central1-docker.pkg.dev/stock-busters-cs115/stock-busters/quantamental-pipeline:latest` |
| **CPU** | 2 cores |
| **Memory** | 4 GB |
| **Timeout** | 3600 seconds (1 hour) |
| **Max Retries** | 1 |

### ML Pipeline Commands

```bash
# Manual execution
gcloud run jobs execute quantamental-pipeline --region=us-central1

# View logs
gcloud run jobs executions logs <execution-id> --region=us-central1

# Update pipeline (after code changes)
docker build -t us-central1-docker.pkg.dev/stock-busters-cs115/stock-busters/quantamental-pipeline:latest .
docker push us-central1-docker.pkg.dev/stock-busters-cs115/stock-busters/quantamental-pipeline:latest
gcloud run jobs update quantamental-pipeline \
    --image=us-central1-docker.pkg.dev/stock-busters-cs115/stock-busters/quantamental-pipeline:latest \
    --region=us-central1

# Scheduler management
gcloud scheduler jobs run trigger-quantamental-pipeline --location=us-central1  # Manual trigger
gcloud scheduler jobs pause trigger-quantamental-pipeline --location=us-central1
gcloud scheduler jobs resume trigger-quantamental-pipeline --location=us-central1
```
## Snapshot Evidence

## Cloud run Deployment on GCP

Base on the time stamp, the ML pipeline is executed successfully every morning at 6AM CST.

<img width="1907" height="581" alt="image" src="https://github.com/user-attachments/assets/ef954c42-3844-44e5-978d-0258dc2b2575" />

**Cloud scheduler set up**

<img width="932" height="585" alt="image" src="https://github.com/user-attachments/assets/6537bc41-7874-48a8-93de-0cafd1e9653b" />

**Cloud Scheduler job**
<img width="1596" height="260" alt="image" src="https://github.com/user-attachments/assets/4f620f5e-6a63-4929-b884-0a6a125c1ff4" />


**GCP deployment**

<img width="814" height="691" alt="image" src="https://github.com/user-attachments/assets/ff982684-734c-47d5-9e1d-0cf77c8e7b9c" />

**GCP Log**

<img width="807" height="932" alt="image" src="https://github.com/user-attachments/assets/c6ba264d-7170-4629-bac6-3d3bdc74c25f" />

**Output link and update on W&B**

<img width="1895" height="846" alt="image" src="https://github.com/user-attachments/assets/61773918-fbad-4205-a4b3-0fe432c46da1" />

**Data versioning is tracked on W&B**

<img width="745" height="343" alt="image" src="https://github.com/user-attachments/assets/72ff0787-f57e-4763-a748-8fa05af93603" />


📄 *See [docs/Quantamental_Model_Pipeline.md](docs/Quantamental_Model_Pipeline.md) for detailed analysis.*
---


## Known Issues and Limitations  <--- Majid/Mahmood/Seraphim/Siri update

### Limitations

|Limitations| Issue | Impact | Mitigation |
|-----------|-------|--------|------------|
|Model| Moderate Prediction Accuracy | Predictions may not reliably identify outperforming stocks | Implement walk-forward validation, additional hyperparameter tuning, and ensemble methods (XGBoost, LightGBM) |
|Storage cost|GCS storage Growth | Output files accumulate over time, increasing storage costs|  Implement lifecycle policies to delete old files, use versioning with retention limits|
|Data Pipeline|Stale Predictions|Same recommendations shown for entire month; doesn't reflect intra-month market changes|Implement daily prediction refresh using latest technical indicators while maintaining monthly model training|


**Bugs and Fixes**
- Rarely the chatbot doesn't activate the generate report button. This happens when the user confirmation is ambiguous. Work is being done to resolve that.
- In dark mode, some of the text is not visible. Working on changing the colors and contrast.

**Future Enhancements**

***Models***
- Incorporate additional models for recommending stocks
- Integrate Sentiment and macroeconomics signals
  
***Product Features***
- Develop auto trader that implements trading orders directly to the brokerage accounts
- Launch mobile alerts for new signal or trade execution
  
***Exploring New Horizons***
- Expand coverage to ETF and cryptocurrencies
- Introduce commodity and alternative asset classes
- Expand product availability to International Markets






---
### Milestone 5 - Code Organization    <-- Seraphim/Mahmood/Majid/Siri  check your part

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
    │
    ├── 📁 deployment/
    │       ├── deploy_images/         # Docker image building and pushing
    │       │   ├── __main__.py        # Pulumi program for building images
    │       │   ├── Pulumi.yaml        # Project configuration
    │       │   └── Pulumi.dev.yaml    # Stack-specific configuration
    │       │
    │       ├── deploy_k8s/            # Kubernetes cluster deployment
    │       │   ├── __main__.py        # Main Pulumi orchestration
    │       │   ├── create_network.py  # VPC, subnet, NAT configuration
    │       │   ├── create_cluster.py  # GKE cluster and node pool setup
    │       │   ├── setup_containers.py # Application deployments
    │       │   ├── setup_loadbalancer.py # Ingress configuration
    │       │   ├── Pulumi.yaml        # Project configuration
    │       │   └── Pulumi.dev.yaml    # Stack-specific configuration
    │       │
    │       ├── deploy_single_vm/      # Legacy single VM deployment (reference only)
    │       │
    │       ├── Dockerfile             # Deployment container image
    │       ├── docker-shell.sh        # Container startup script
    │       ├── docker-entrypoint.sh   # Container initialization
    │       ├── pyproject.toml         # Python dependencies
    │       ├── Readme.md              # Readme file
    │       └── uv.lock                # Locked dependencies
    ├── dvc.yaml                           ← data versioning
    ├── requirements.txt
    ├── README.md
    └── .env.example  
```


































