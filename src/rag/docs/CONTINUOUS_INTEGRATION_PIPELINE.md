# Continuous Integration Pipeline

## Overview

The RAG component uses a comprehensive CI/CD pipeline built on GitHub Actions that automatically builds, tests, and validates code changes. The pipeline ensures code quality, maintains test coverage standards, and provides fast feedback on pull requests and commits.

**Pipeline Location**: `.github/workflows/ci-rag.yml`

## Pipeline Architecture

The CI pipeline consists of **6 sequential jobs** that run in parallel where possible:

```
┌─────────┐
│  Build  │ (Job 1: Builds Docker image once, shared by all jobs)
└────┬────┘
     │
     ├───► Lint & Format (Job 2)
     ├───► Unit Tests (Job 3)
     ├───► Integration Tests (Job 4)
     └───► System Tests (Job 5)
           │
           └───► Test Summary (Job 6: Aggregates results)
```

### Key Design Principles

1. **Single Build**: Docker image is built once and shared across all test jobs (saves ~3-4 minutes)
2. **Parallel Execution**: Lint, unit, and integration tests run simultaneously after build
3. **Docker-Based**: All tests run inside Docker containers for consistency
4. **Fast Feedback**: Fails fast with `--maxfail` flags to surface issues quickly
5. **Coverage Tracking**: Enforces minimum 50% code coverage requirement

## When the Pipeline Runs

The pipeline automatically triggers on:

- **Push events**: When code is pushed to `main`, `develop`, or `Milestone4` branches
- **Pull requests**: When PRs target `main`, `develop`, or `Milestone4` branches
- **Path filtering**: Only runs when files in `src/rag/**` are modified
- **Manual trigger**: Can be manually triggered via `workflow_dispatch`

**Concurrency Control**: Only one pipeline runs per branch at a time. New commits cancel in-progress runs.

## Pipeline Jobs

### Job 1: Build Docker Image

**Purpose**: Build the RAG service Docker image that will be used by all subsequent jobs.

**Steps**:
1. Checkout repository code
2. Set up Docker Buildx for advanced build features
3. Create dummy GCS key file (if missing) for build context
4. Build Docker image with:
   - **Tag**: `rag-service:${{ github.sha }}` (commit SHA for uniqueness)
   - **Cache**: Uses GitHub Actions cache (`type=gha`) for faster builds
   - **Context**: Project root (`.`)
   - **Dockerfile**: `./src/rag/Dockerfile`
5. Verify image exists and is inspectable
6. Save image as tar archive
7. Upload as artifact for other jobs

**Timeout**: 6 minutes  
**Output**: Docker image artifact (`docker-image`)

**Why This Matters**: Building once and sharing saves significant time compared to building in each job.

---

### Job 2: Lint and Format Check

**Purpose**: Ensure code follows Python style guidelines and formatting standards.

**Dependencies**: Requires `build` job to complete

**Steps**:
1. Download and load Docker image from build job
2. Run code quality checks:
   - **Black**: Formatting check (`--check` mode, line length 120)
   - **Flake8**: Linting check (max line length 120, ignores specific warnings)

**Timeout**: 3 minutes  
**Failure Impact**: Pipeline fails if code doesn't meet style standards

**Tools Used**:
- `black --check --line-length 120 rag.py`
- `flake8 --max-line-length=120 --extend-ignore=E203,W503,E501,E722,W504,E402,F401,F841,F811,F821 rag.py`

---

### Job 3: Unit Tests + Coverage

**Purpose**: Run unit tests and measure code coverage to ensure minimum 50% coverage.

**Dependencies**: Requires `build` job to complete

**Steps**:
1. Checkout code (for coverage report paths)
2. Download and load Docker image
3. Run unit tests with coverage:
   - **Test marker**: `-m unit` (only unit tests)
   - **Coverage tool**: `pytest-cov`
   - **Coverage reports**: 
     - Terminal output
     - XML: `coverage/coverage.xml` (for CI integration)
     - HTML: `coverage/htmlcov/` (for detailed browsing)
   - **Coverage threshold**: `--cov-fail-under=50` (fails if < 50%)
   - **Fast failure**: `--maxfail=2 -x` (stops after 2 failures)
4. Upload coverage reports as artifacts (retained 7 days)

**Timeout**: 5 minutes  
**Environment Variables**:
```bash
CHROMADB_HOST=localhost
CHROMADB_PORT=8000
VECTOR_COLLECTION=test_collection
GCS_BUCKET_NAME=""
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
ENABLE_CACHE=0
AUTO_START_CHROMADB=0
GOOGLE_APPLICATION_CREDENTIALS=""
```

**Coverage Requirements**:
- **Minimum**: 50% (enforced by `--cov-fail-under=50`)
- **Current**: ~73% (exceeds requirement)
- **Reports**: Available as downloadable artifacts

---

### Job 4: Integration Tests

**Purpose**: Test component interactions with mocked external services.

**Dependencies**: Requires `build` job to complete

**Steps**:
1. Download and load Docker image
2. Run integration tests:
   - **Test marker**: `-m integration` (only integration tests)
   - **Fast failure**: `--maxfail=1 -x` (stops after 1 failure)
   - **Quiet mode**: `-q` (minimal output)

**Timeout**: 4 minutes  
**Environment Variables**: Same as unit tests

**What Integration Tests Cover**:
- FastAPI endpoint interactions
- ChromaDB client operations (mocked)
- GCS operations (mocked)
- API request/response handling

---

### Job 5: System Tests

**Purpose**: Test the complete system with a running server instance.

**Dependencies**: Requires `build` job to complete

**Conditional Execution**: Only runs on:
- `main` branch
- `develop` branch
- `Milestone4` branch
- Manual workflow dispatch

**Steps**:
1. Download and load Docker image
2. Start RAG server container:
   - **Ports**: 9000 (API), 8000 (ChromaDB)
   - **Environment**: Development mode (`DEV=1`)
   - **Detached mode**: Runs in background
3. Wait for server readiness:
   - Polls `/health` endpoint
   - Maximum 10 attempts (20 seconds total)
   - Fails if server doesn't become ready
4. Run system tests:
   - **Test marker**: `-m system` (only system tests)
   - **Network**: Uses `--network host` to access running server
   - **Fast failure**: `--maxfail=1 -x`
5. Show server logs (always, for debugging)
6. Stop and remove server container (always, cleanup)

**Timeout**: 5 minutes  
**What System Tests Cover**:
- Full API endpoint functionality
- Server startup and health checks
- End-to-end query processing
- Real HTTP requests/responses

**Why Conditional**: System tests are slower and require a running server. Skipping on feature branches speeds up development feedback.

---

### Job 6: Test Summary

**Purpose**: Aggregate test results, extract coverage metrics, and provide summary.

**Dependencies**: Requires all previous jobs (`build`, `lint-and-format`, `unit-tests`, `integration-tests`, `system-tests`)

**Execution**: Always runs (`if: always()`) to provide summary even if tests fail

**Steps**:
1. Download coverage report artifact
2. Extract coverage percentage from XML report
3. Check test results from all jobs
4. Generate GitHub Actions summary:
   - Test status table (✅ Passed / ❌ Failed)
   - Coverage percentage
   - Links to coverage reports
5. Send Slack notification (if webhook configured):
   - Success/failure status
   - Repository and branch info
   - Test results breakdown
   - Links to commit and workflow run

**Output**: 
- GitHub Actions step summary (visible in Actions UI)
- Optional Slack notification

---

## Test Types and Coverage

### Unit Tests (`tests/unit/`)

**Purpose**: Test individual functions and classes in isolation.

**Characteristics**:
- Fast execution (~2-3 seconds for 163 tests)
- Heavy use of mocking (no external dependencies)
- High coverage of core logic
- Test files:
  - `test_rag_core.py`: Core RAG functions, internals, utilities
  - `test_rag_ingestion.py`: Ingestion pipeline, PDF processing
  - `test_rag_infrastructure.py`: CLI, GCS sync, Retriever

**Coverage**: ~73% of codebase

### Integration Tests (`tests/integration/`)

**Purpose**: Test component interactions with mocked services.

**Characteristics**:
- Tests API endpoints with mocked ChromaDB/GCS
- Validates request/response handling
- Tests error handling and edge cases
- ~15 tests

**Coverage**: API layer and service integrations

### System Tests (`tests/system/`)

**Purpose**: Test complete system with running server.

**Characteristics**:
- Real HTTP requests to running server
- End-to-end query processing
- Server health and readiness checks
- ~8 tests

**Coverage**: Full system behavior

---

## Coverage Requirements

### Minimum Coverage: 50%

The pipeline enforces a minimum of **50% code coverage** using `--cov-fail-under=50`. If coverage drops below this threshold, the pipeline fails.

### Current Coverage: ~73%

The RAG component currently maintains **~73% code coverage**, significantly exceeding the minimum requirement.

### Coverage Reports

Coverage reports are generated in multiple formats:

1. **Terminal Output**: Shown in CI logs with missing line numbers
2. **XML Report**: `coverage/coverage.xml` - For CI/CD integration
3. **HTML Report**: `coverage/htmlcov/index.html` - For detailed browsing

**Access**: Coverage reports are available as downloadable artifacts from the GitHub Actions UI (retained for 7 days).

---

## Running Tests Locally

You can run the same tests locally using Docker:

### Build the Image
```bash
docker build -t rag-service:local -f src/rag/Dockerfile .
```

### Run Unit Tests
```bash
docker run --rm \
  -v "${PWD}/src/rag:/workspace" \
  -e PYTHONPATH="/.venv/lib/python3.12/site-packages:$PYTHONPATH" \
  rag-service:local \
  pytest tests/unit/ --cov=rag --cov-report=term --cov-report=html -m unit
```

### Run Integration Tests
```bash
docker run --rm \
  -e PYTHONPATH="/.venv/lib/python3.12/site-packages:$PYTHONPATH" \
  rag-service:local \
  pytest tests/integration/ -m integration
```

### Run System Tests
```bash
# Start server
docker run -d --name rag-server -p 9000:9000 rag-service:local

# Wait for server
curl http://localhost:9000/health

# Run tests
docker run --rm --network host \
  -e PYTHONPATH="/.venv/lib/python3.12/site-packages:$PYTHONPATH" \
  -e API_BASE_URL=http://localhost:9000 \
  rag-service:local \
  pytest tests/system/ -m system

# Cleanup
docker stop rag-server && docker rm rag-server
```

---

## Pipeline Performance

### Typical Execution Times

- **Build**: ~2-3 minutes (with cache) / ~4-5 minutes (without cache)
- **Lint & Format**: ~30 seconds
- **Unit Tests**: ~3-4 minutes (includes coverage analysis)
- **Integration Tests**: ~1-2 minutes
- **System Tests**: ~2-3 minutes
- **Test Summary**: ~10 seconds

**Total Pipeline Time**: ~8-12 minutes (with cache) / ~12-16 minutes (without cache)

### Optimization Strategies

1. **Docker Layer Caching**: Uses GitHub Actions cache for Docker layers
2. **Parallel Execution**: Lint, unit, and integration tests run simultaneously
3. **Fast Failure**: Tests stop early on failures (`--maxfail`, `-x`)
4. **Conditional System Tests**: Only run on main branches
5. **Artifact Sharing**: Single build shared across all jobs

---

## Troubleshooting

### Pipeline Fails on Linting

**Problem**: Black or Flake8 reports formatting/linting errors.

**Solution**:
```bash
# Format code
docker run --rm -v "${PWD}/src/rag:/workspace" rag-service:local \
  black --line-length 120 rag.py

# Check linting
docker run --rm -v "${PWD}/src/rag:/workspace" rag-service:local \
  flake8 --max-line-length=120 rag.py
```

### Coverage Below 50%

**Problem**: Coverage drops below minimum threshold.

**Solution**:
1. Review coverage report to identify uncovered code
2. Add tests for missing coverage
3. Focus on critical paths first
4. Use `pytest --cov=rag --cov-report=html` to see detailed HTML report

### System Tests Fail

**Problem**: System tests fail with connection errors.

**Possible Causes**:
- Server not starting properly
- Health endpoint not responding
- Port conflicts

**Solution**:
1. Check server logs in CI output
2. Verify server starts locally: `docker run -p 9000:9000 rag-service:local`
3. Test health endpoint: `curl http://localhost:9000/health`
4. Review system test logs for specific errors

### Tests Timeout

**Problem**: Tests exceed timeout limits.

**Solution**:
1. Check for infinite loops or hanging operations
2. Review test execution time locally
3. Consider optimizing slow tests
4. Increase timeout if test is legitimately slow

### Docker Build Fails

**Problem**: Docker image build fails.

**Possible Causes**:
- Missing dependencies in `pyproject.toml`
- Dockerfile syntax errors
- Build context issues

**Solution**:
1. Test build locally: `docker build -t rag-service:test -f src/rag/Dockerfile .`
2. Check Dockerfile syntax
3. Verify all dependencies are listed
4. Review build logs for specific errors

---

## CI Configuration Details

### Environment Variables

All test jobs use consistent environment variables to ensure reproducible test execution:

```bash
CHROMADB_HOST=localhost
CHROMADB_PORT=8000
VECTOR_COLLECTION=test_collection
GCS_BUCKET_NAME=""  # Empty to disable GCS operations
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
ENABLE_CACHE=0  # Disable caching for tests
AUTO_START_CHROMADB=0  # Don't start ChromaDB server
GOOGLE_APPLICATION_CREDENTIALS=""  # No GCS credentials
```

### Pytest Configuration

Tests use configuration from `src/rag/pytest.ini`:

- **Test discovery**: `testpaths = tests`
- **Test patterns**: `test_*.py` files, `Test*` classes, `test_*` functions
- **Markers**: `unit`, `integration`, `system`, `slow`
- **Output**: Verbose with short tracebacks

### Docker Image Tagging

- **CI builds**: `rag-service:${{ github.sha }}` (commit SHA)
- **Local builds**: `rag-service:local` (or any custom tag)

---

## Best Practices

### Before Pushing

1. **Run tests locally**: Ensure all tests pass before pushing
2. **Check formatting**: Run `black` to format code
3. **Verify coverage**: Run with `--cov` to ensure coverage stays above 50%
4. **Review changes**: Make sure changes are focused and well-tested

### Writing Tests

1. **Use appropriate markers**: Mark tests as `@pytest.mark.unit`, `@pytest.mark.integration`, or `@pytest.mark.system`
2. **Mock external dependencies**: Unit tests should not make real network calls
3. **Test edge cases**: Include tests for empty inputs, None values, error conditions
4. **Keep tests fast**: Unit tests should complete in < 1 second each
5. **Maintain coverage**: Add tests when adding new code paths

### Debugging Failed Pipelines

1. **Check job logs**: Each job has detailed logs in GitHub Actions
2. **Download artifacts**: Coverage reports and logs are available as artifacts
3. **Reproduce locally**: Run the same commands locally to debug
4. **Review recent changes**: Check what changed that might have caused the failure

---

## Integration with Development Workflow

### Pull Request Workflow

1. **Create PR**: Push changes to feature branch
2. **CI Runs**: Pipeline automatically runs on PR creation/updates
3. **Review Results**: Check CI status in PR checks
4. **Fix Issues**: Address any failures before requesting review
5. **Merge**: PR can be merged when CI passes

### Commit Workflow

1. **Push to Branch**: Pipeline runs automatically
2. **Monitor Status**: Check Actions tab for pipeline status
3. **Fix if Needed**: Address failures before merging
4. **Deploy**: After merge to main, code is ready for deployment

---

## Future Enhancements

Potential improvements to the CI pipeline:

1. **Parallel Test Execution**: Use `pytest-xdist` to run tests in parallel
2. **Test Caching**: Cache test results for unchanged files
3. **Matrix Testing**: Test against multiple Python versions
4. **Performance Benchmarks**: Track test execution time over time
5. **Security Scanning**: Add security vulnerability scanning
6. **Dependency Updates**: Automatically check for dependency updates

---

## Summary

The RAG CI pipeline provides:

 **Automated Quality Checks**: Linting, formatting, and style validation  
 **Comprehensive Testing**: Unit, integration, and system tests  
 **Coverage Enforcement**: Minimum 50% coverage requirement (currently ~73%)  
 **Fast Feedback**: Parallel execution and fast failure modes  
 **Consistent Environment**: Docker-based testing ensures reproducibility  
 **Detailed Reporting**: Coverage reports and test summaries  
 **Optional Notifications**: Slack integration for team awareness  

The pipeline ensures code quality and reliability while providing fast feedback to developers.

