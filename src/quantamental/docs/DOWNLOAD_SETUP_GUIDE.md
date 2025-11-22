# 📥 DOWNLOAD & SETUP GUIDE - Step by Step

## 🎯 Where Your Files Are Located

All files are in Claude's interface. Here's how to download them:

---

## 📦 Method 1: Download Individual Files (Recommended)

### Files in the Chat Interface

Look for the **file links** in this chat. Click each one to download:

**Core CI Configuration Files (MUST HAVE):**
1. `Dockerfile` (updated)
2. `docker-shell.sh` 
3. `pytest.ini`
4. `.flake8`
5. `.pre-commit-config.yaml`
6. `.github/workflows/ci.yml` (updated)

**Test Files (MUST HAVE):**
7. `tests/test_data_collect.py`
8. `tests/test_system.py`

**Documentation (HELPFUL):**
9. `CI_SETUP.md`
10. `TESTING_STRATEGY.md`
11. `COVERAGE_GUIDE.md`
12. `MS4_CI_REQUIREMENTS_EXPLAINED.md`

---

## 📂 Method 2: Download from Outputs Folder

All files are in: `/mnt/user-data/outputs/quantamental/`

You can see download links in the Claude interface for each file.

---

## 🗂️ Where to Put Each File

Here's EXACTLY where each file goes in your project:

```
Your Project Folder Structure:
C:\Users\YourName\quantamental\    ← Your project root

├── .github\
│   └── workflows\
│       └── ci.yml                 ← REPLACE existing file
│
├── tests\
│   ├── __init__.py               ← Keep existing
│   ├── test_utils.py             ← Keep existing
│   ├── test_data_collect.py      ← ADD NEW FILE
│   └── test_system.py            ← ADD NEW FILE
│
├── data_collect.py               ← Keep (your existing file)
├── data_process.py               ← Keep
├── model_train.py                ← Keep
├── model_predict.py              ← Keep
├── backtest.py                   ← Keep
├── main.py                       ← Keep
├── utils.py                      ← Keep
├── config.yaml                   ← Keep
├── requirements.txt              ← Keep
│
├── Dockerfile                     ← REPLACE with new version
├── docker-shell.sh               ← ADD NEW FILE
├── pytest.ini                    ← ADD NEW FILE
├── .flake8                       ← ADD NEW FILE
├── .pre-commit-config.yaml       ← ADD NEW FILE
│
├── CI_SETUP.md                   ← ADD NEW (documentation)
├── TESTING_STRATEGY.md           ← ADD NEW (documentation)
├── COVERAGE_GUIDE.md             ← ADD NEW (documentation)
├── MS4_CI_REQUIREMENTS_EXPLAINED.md ← ADD NEW (documentation)
└── README.md                     ← Keep your existing
```

---

## 🔄 Step-by-Step Setup Process

### Step 1: Create Backup (IMPORTANT!)

```powershell
# In PowerShell, from your project folder
cd C:\path\to\your\quantamental

# Create backup
Copy-Item -Recurse . ..\quantamental_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')
```

### Step 2: Download Core Files

Download these files from Claude interface:

**Priority 1 (Must Have):**
- [ ] `Dockerfile`
- [ ] `docker-shell.sh`
- [ ] `pytest.ini`
- [ ] `.flake8`
- [ ] `.pre-commit-config.yaml`
- [ ] `.github/workflows/ci.yml`

**Priority 2 (Test Files):**
- [ ] `tests/test_data_collect.py`
- [ ] `tests/test_system.py`

**Priority 3 (Documentation):**
- [ ] All the `*.md` files

### Step 3: Place Files in Correct Locations

```powershell
# In your project folder
cd C:\path\to\your\quantamental

# Make sure .github\workflows folder exists
New-Item -ItemType Directory -Force -Path .github\workflows

# Copy downloaded files to correct locations:

# Core config files (in root)
Copy-Item Downloads\Dockerfile .
Copy-Item Downloads\docker-shell.sh .
Copy-Item Downloads\pytest.ini .
Copy-Item Downloads\.flake8 .
Copy-Item Downloads\.pre-commit-config.yaml .

# CI workflow
Copy-Item Downloads\ci.yml .github\workflows\

# Test files
Copy-Item Downloads\test_data_collect.py tests\
Copy-Item Downloads\test_system.py tests\

# Documentation (optional but helpful)
Copy-Item Downloads\*.md .
```

### Step 4: Make docker-shell.sh Executable

```powershell
# If using Git Bash or WSL
chmod +x docker-shell.sh
```

### Step 5: Verify File Structure

```powershell
# Check that all files are in place
Get-ChildItem -Recurse | Where-Object {$_.Name -match "(Dockerfile|docker-shell|pytest|flake8|pre-commit|ci.yml|test_.*\.py)"}
```

---

## ✅ Verification Checklist

After copying files, verify:

### Root Directory Files:
```powershell
# Should see these files in root:
ls -Name Dockerfile, docker-shell.sh, pytest.ini, .flake8, .pre-commit-config.yaml
```

### .github Folder:
```powershell
# Should see:
ls .github\workflows\ci.yml
```

### tests Folder:
```powershell
# Should see:
ls tests\
# Output should include:
# __init__.py (existing)
# test_utils.py (existing)
# test_data_collect.py (NEW)
# test_system.py (NEW)
```

---

## 🔧 File-by-File Replacement Guide

### Files to REPLACE (overwrite existing):

#### 1. **Dockerfile** ✏️ REPLACE
**Why:** Added testing tools (pytest, flake8, black)

**Location:** Root directory

**Action:**
```powershell
# Backup old version first
Copy-Item Dockerfile Dockerfile.backup

# Then copy new version
Copy-Item Downloads\Dockerfile .
```

#### 2. **.github/workflows/ci.yml** ✏️ REPLACE
**Why:** Enhanced with coverage checks and Docker testing

**Location:** `.github\workflows\ci.yml`

**Action:**
```powershell
# Backup old version
Copy-Item .github\workflows\ci.yml .github\workflows\ci.yml.backup

# Copy new version
Copy-Item Downloads\ci.yml .github\workflows\
```

### Files to ADD (new files):

#### 3. **docker-shell.sh** ➕ NEW
**Location:** Root directory

```powershell
Copy-Item Downloads\docker-shell.sh .
```

#### 4. **pytest.ini** ➕ NEW
**Location:** Root directory

```powershell
Copy-Item Downloads\pytest.ini .
```

#### 5. **.flake8** ➕ NEW
**Location:** Root directory

```powershell
Copy-Item Downloads\.flake8 .
```

#### 6. **.pre-commit-config.yaml** ➕ NEW
**Location:** Root directory

```powershell
Copy-Item Downloads\.pre-commit-config.yaml .
```

#### 7. **tests/test_data_collect.py** ➕ NEW
**Location:** `tests\` folder

```powershell
Copy-Item Downloads\test_data_collect.py tests\
```

#### 8. **tests/test_system.py** ➕ NEW
**Location:** `tests\` folder

```powershell
Copy-Item Downloads\test_system.py tests\
```

---

## 🚀 After Setup - First Test

### Step 1: Build Docker Image Locally

```powershell
# From your project root
docker build -t quantamental-dev .
```

**Expected output:**
```
Successfully built quantamental-dev
```

### Step 2: Enter Container (Test docker-shell.sh)

```bash
# Using Git Bash on Windows
bash docker-shell.sh
```

**OR manually:**
```powershell
docker run -it --rm quantamental-dev bash
```

### Step 3: Inside Container - Run Tests

```bash
# Inside the container
pytest tests/ -v

# Check coverage
pytest tests/ --cov=. --cov-report=term-missing
```

**Expected output:**
```
tests/test_utils.py::test_validate_dataframe_success PASSED
tests/test_data_collect.py::test_fetch_sp500_tickers_returns_list PASSED
...
---------- coverage: ----------
TOTAL    910    xxx    XX%
```

### Step 4: Exit Container

```bash
exit
```

---

## 📋 Common Issues & Fixes

### Issue 1: "docker-shell.sh not found"

**Fix:**
```powershell
# Make sure file is in root and executable
ls docker-shell.sh

# If using Git Bash
chmod +x docker-shell.sh
```

### Issue 2: "pytest: command not found" inside container

**Fix:** Rebuild Docker image
```powershell
docker build --no-cache -t quantamental-dev .
```

### Issue 3: ".flake8 file not showing"

**Fix:** Windows hides files starting with "."
```powershell
# Show hidden files in File Explorer: View → Show → Hidden items

# Or in PowerShell
Get-ChildItem -Force | Where-Object {$_.Name -like ".*"}
```

### Issue 4: "Module not found" errors in tests

**Fix:** Ensure `__init__.py` exists
```powershell
# Check if exists
ls tests\__init__.py

# If not, create it
New-Item -ItemType File -Path tests\__init__.py
```

---

## 🎯 Quick Start Commands

After all files are in place:

```powershell
# 1. Set environment variables (Windows PowerShell)
$env:WANDB_API_KEY="your_key_here"
$env:GCS_BUCKET_NAME="your_bucket"
$env:FMP_API_KEY="your_key"

# 2. Build image
docker build -t quantamental-dev .

# 3. Enter container (using Git Bash)
bash docker-shell.sh

# 4. Inside container - run tests
pytest tests/ -v --cov=. --cov-report=term-missing

# 5. Set up pre-commit hooks
pre-commit install
pre-commit run --all-files

# 6. Exit
exit
```

---

## 📤 After Testing Locally - Push to GitHub

```powershell
# Add all new files
git add .

# Commit
git commit -m "feat: Add MS4 CI/CD pipeline with comprehensive testing"

# Push
git push origin main
```

**Then:**
1. Go to GitHub repository
2. Click "Actions" tab
3. Wait ~5 minutes for CI to run
4. Take screenshot when all checks are green ✅

---

## 📊 What Each File Does

| File | Purpose |
|------|---------|
| **Dockerfile** | Container definition with testing tools |
| **docker-shell.sh** | Easy entry into dev container |
| **pytest.ini** | Test configuration & coverage settings |
| **.flake8** | Linting rules (style checking) |
| **.pre-commit-config.yaml** | Automated pre-commit checks |
| **ci.yml** | GitHub Actions CI/CD pipeline |
| **test_data_collect.py** | Integration tests template |
| **test_system.py** | End-to-end system tests |

---

## 🎓 Next Steps After Setup

1. ✅ Verify all files are in place
2. ✅ Test Docker build works
3. ✅ Run tests locally
4. 📝 **Write more tests** to reach 50% coverage
5. 🚀 Push to GitHub
6. 📸 Screenshot passing CI for MS4

---

## 💡 Pro Tips

1. **Keep backups** - Always backup before replacing files
2. **Test locally first** - Don't push untested changes
3. **Read the docs** - Check the `.md` files for detailed info
4. **Use Git** - Commit often with meaningful messages
5. **Ask for help** - If something doesn't work, debug step by step

---

## 📞 Troubleshooting Checklist

If something doesn't work:

- [ ] Did you place files in correct locations?
- [ ] Did you rebuild Docker image after changes?
- [ ] Are environment variables set?
- [ ] Is Docker running?
- [ ] Are all files downloaded (check file sizes)?
- [ ] Did you commit all files to git?

---

**You're ready to set up your MS4 CI pipeline! Start with downloading the files.** 🚀

**Need help with a specific step? Let me know!** 💪
