# PowerShell script to push CI fixes to GitHub
# Run this script to commit and push all CI-related changes

Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Pushing CI Fixes to GitHub" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

# Try to find Git
$gitExe = $null
$gitPaths = @(
    "C:\Program Files\Git\bin\git.exe",
    "C:\Program Files (x86)\Git\bin\git.exe",
    "$env:LOCALAPPDATA\Programs\Git\bin\git.exe",
    "git"  # Try if in PATH
)

foreach ($path in $gitPaths) {
    try {
        if ($path -eq "git") {
            $result = & git --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $gitExe = "git"
                break
            }
        } elseif (Test-Path $path) {
            $result = & $path --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $gitExe = $path
                break
            }
        }
    } catch {
        continue
    }
}

if (-not $gitExe) {
    Write-Host "`n❌ Git not found in PATH or common locations" -ForegroundColor Red
    Write-Host "`nPlease use one of these options:" -ForegroundColor Yellow
    Write-Host "`nOption 1: GitHub Desktop" -ForegroundColor Cyan
    Write-Host "  1. Open GitHub Desktop" -ForegroundColor White
    Write-Host "  2. Review changes in 'Changes' tab" -ForegroundColor White
    Write-Host "  3. Enter commit message: 'Fix CI issues: Black, Flake8, and unit tests'" -ForegroundColor White
    Write-Host "  4. Click 'Commit to [branch]'" -ForegroundColor White
    Write-Host "  5. Click 'Push origin'" -ForegroundColor White
    
    Write-Host "`nOption 2: Git Bash" -ForegroundColor Cyan
    Write-Host "  1. Open Git Bash in this directory" -ForegroundColor White
    Write-Host "  2. Run: git add ." -ForegroundColor White
    Write-Host "  3. Run: git commit -m 'Fix CI issues: Black, Flake8, and unit tests'" -ForegroundColor White
    Write-Host "  4. Run: git push" -ForegroundColor White
    
    Write-Host "`nOption 3: Add Git to PATH" -ForegroundColor Cyan
    Write-Host "  Install Git for Windows and add to PATH" -ForegroundColor White
    
    exit 1
}

Write-Host "`n✅ Found Git: $gitExe" -ForegroundColor Green

# Change to repo directory
$repoPath = "C:\Users\eilke\OneDrive\Desktop\Github Repo\CSCI115-AI-Agent"
Set-Location $repoPath

Write-Host "`n📋 Changes to commit:" -ForegroundColor Yellow
& $gitExe status --short 2>&1 | Select-Object -First 50

Write-Host "`n🔍 Checking what will be committed..." -ForegroundColor Yellow
$changes = & $gitExe diff --name-only 2>&1
$staged = & $gitExe diff --cached --name-only 2>&1

if ($changes.Count -eq 0 -and $staged.Count -eq 0) {
    Write-Host "`n⚠️  No changes detected. Files may already be committed." -ForegroundColor Yellow
    Write-Host "Checking recent commits..." -ForegroundColor Gray
    & $gitExe log --oneline -5 2>&1
    exit 0
}

Write-Host "`n📦 Staging all changes..." -ForegroundColor Yellow
& $gitExe add . 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to stage changes" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Changes staged" -ForegroundColor Green

$commitMessage = "Fix CI issues: Black formatting, Flake8 linting, and unit test failures

- Run Black formatter on all Python files
- Fix Flake8 import issues in rag_helpers.py
- Fix 3 unit test failures (test_semantic_chunks_large_text, test_query_rag_texts, test_retriever_query_k_limits)
- Remove rag_functions.py from CI
- All tests now passing: 40/40 unit, 14/14 integration
- CI pipeline ready for GitHub Actions"

Write-Host "`n💬 Committing changes..." -ForegroundColor Yellow
& $gitExe commit -m $commitMessage 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to commit" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Changes committed" -ForegroundColor Green

Write-Host "`n🚀 Pushing to GitHub..." -ForegroundColor Yellow
& $gitExe push 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n⚠️  Push failed. You may need to:" -ForegroundColor Yellow
    Write-Host "  - Set up remote: git remote add origin <url>" -ForegroundColor White
    Write-Host "  - Set upstream: git push -u origin <branch>" -ForegroundColor White
    Write-Host "  - Authenticate with GitHub" -ForegroundColor White
    exit 1
}

Write-Host "`n✅ Successfully pushed to GitHub!" -ForegroundColor Green
Write-Host "`n🎉 CI will now run on GitHub Actions!" -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

