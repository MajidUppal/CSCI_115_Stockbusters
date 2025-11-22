# CI/CD Setup Guide - MS4
## Quantamental Stock Screening Pipeline

This guide explains how to use the CI/CD pipeline for MS4 submission.

---

## 📁 File Structure

```
quantamental/
├── .github/workflows/
│   └── ci.yml                    # GitHub Actions CI pipeline
├── tests/
│   ├── __init__.py
│   ├── test_utils.py             # Utility tests
│   └── test_data_collect.py      # Data collection tests
├── data_collect.py
├── data_process.py
├── model_train.py
├── model_predict.py
├── backtest.py
├── main.py
├── utils.py
├── Dockerfile                    # Container definition
├── docker-shell.sh              # Development container entry
├── pytest.ini                   # Test configuration
├── .flake8                      # Linting configuration
├── .pre-commit-config.yaml      # Pre-commit hooks
└── requirements.txt
```

---

## 🚀 Quick Start

### 1. Local Development with Docker

```bash
# Make docker-shell.sh executable
chmod +x docker-shell.sh

# Set environment variables
export WANDB_API_KEY="your_wandb_key"
export GCS_BUCKET_NAME="your_bucket_name"
export FMP_API_KEY="your_fmp_key"

# Enter development container
./docker-shell.sh
```

### 2. Inside the Container

```bash
# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=. --cov-report=term-missing

# Lint code
flake8 *.py

# Format code
black *.py

# Run the pipeline
python main.py
```

---

## 🔧 Setting Up Pre-commit Hooks

Pre-commit hooks automatically run checks before each commit.

```bash
# Inside the container
pre-commit install

# Run manually on all files
pre-commit run --all-files

# Now every commit will:
# 1. Format code with Black
# 2. Lint with Flake8
# 3. Sort imports
# 4. Check for common issues
```

---

## 🧪 Writing Tests

### Test File Naming Convention
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test Structure

```python
"""tests/test_your_module.py"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from your_module import your_function

@pytest.mark.unit
def test_your_function_basic():
    """Test basic functionality."""
    result = your_function(input_data)
    assert result == expected_output

@pytest.mark.integration
def test_module_integration():
    """Test integration between modules."""
    # Test multi-module workflow
    pass
```

### Test Markers

- `@pytest.mark.unit` - Fast unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Tests that take time
- `@pytest.mark.api` - Tests requiring API calls

Run specific tests:
```bash
pytest tests/ -m unit           # Only unit tests
pytest tests/ -m "not slow"     # Skip slow tests
pytest tests/ -v -k "test_utils"  # Only utils tests
```

---

## 📊 Coverage Requirements

MS4 requires **60% code coverage minimum**.

```bash
# Check coverage
pytest tests/ --cov=. --cov-report=term-missing

# Generate HTML report
pytest tests/ --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

---

## 🔄 GitHub Actions CI Pipeline

The CI pipeline runs automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

### Pipeline Stages

1. **Code Quality** (`lint-and-format`)
   - Flake8 linting
   - Black formatting check
   - Import sorting check

2. **Testing** (`test`)
   - Run all pytest tests
   - Generate coverage report
   - Upload to Codecov

3. **Docker Build** (`docker-build`)
   - Build Docker image
   - Test image functionality
   - Run tests inside container

4. **Summary** (`integration-summary`)
   - Generate CI summary

### Viewing Results

1. Go to your GitHub repository
2. Click "Actions" tab
3. Select a workflow run
4. View logs and artifacts

---

## 🔐 GitHub Secrets

Add these secrets to your repository:
- `WANDB_API_KEY` - Weights & Biases API key
- `FMP_API_KEY` - Financial Modeling Prep API key
- `GCS_BUCKET_NAME` - Google Cloud Storage bucket

**How to add secrets:**
1. Go to repository Settings
2. Secrets and variables → Actions
3. New repository secret

---

## 🐛 Troubleshooting

### Problem: Tests fail locally but pass in CI
```bash
# Clear cache and rerun
pytest tests/ --cache-clear -v
```

### Problem: Import errors in tests
```python
# Add this to your test file
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

### Problem: Docker build fails
```bash
# Check Dockerfile syntax
docker build -t test-image .

# View build logs
docker build --no-cache -t test-image . 2>&1 | tee build.log
```

### Problem: Pre-commit hooks fail
```bash
# Update hooks
pre-commit autoupdate

# Skip hooks for urgent commit
git commit --no-verify -m "message"
```

---

## ✅ MS4 Submission Checklist

Before submitting:

- [ ] All tests pass: `pytest tests/ -v`
- [ ] Coverage ≥ 60%: `pytest tests/ --cov=.`
- [ ] Code is linted: `flake8 *.py`
- [ ] Code is formatted: `black --check *.py`
- [ ] Docker builds successfully: `docker build -t quantamental .`
- [ ] GitHub Actions CI passes (green checkmark)
- [ ] Pre-commit hooks installed and working
- [ ] All modules have corresponding test files

---

## 📚 Additional Resources

- **pytest docs**: https://docs.pytest.org/
- **flake8 docs**: https://flake8.pycqa.org/
- **black docs**: https://black.readthedocs.io/
- **pre-commit docs**: https://pre-commit.com/
- **GitHub Actions**: https://docs.github.com/actions

---

## 👥 Team Stock Busters

For questions, contact team members or check the course Slack channel.

**Remember**: The goal is production-ready code with automated testing! 🚀
