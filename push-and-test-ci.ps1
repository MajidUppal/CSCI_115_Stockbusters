# PowerShell script to push changes and trigger CI
# Run this script from the repository root

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Push CI/CD Changes and Trigger GitHub Actions" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Try to find Git
$gitExe = $null
$gitPaths = @(
    "C:\Program Files\Git\bin\git.exe",
    "C:\Program Files (x86)\Git\bin\git.exe",
    "$env:LOCALAPPDATA\Programs\Git\bin\git.exe",
    "$env:ProgramFiles\Git\cmd\git.exe",
    "git"  # Try if in PATH
)

foreach ($path in $gitPaths) {
    if ($path -eq "git") {
        try {
            $version = & git --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $gitExe = "git"
                Write-Host "✅ Found Git in PATH" -ForegroundColor Green
                break
            }
        } catch {
            continue
        }
    } elseif (Test-Path $path) {
        $gitExe = $path
        Write-Host "✅ Found Git at: $path" -ForegroundColor Green
        break
    }
}

if (-not $gitExe) {
    Write-Host "❌ Git not found. Please:" -ForegroundColor Red
    Write-Host "   1. Install Git from https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "   2. Or use GitHub Desktop" -ForegroundColor Yellow
    Write-Host "   3. Or run commands manually in Git Bash" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Manual steps:" -ForegroundColor Cyan
    Write-Host "   git add ." -ForegroundColor White
    Write-Host "   git commit -m 'feat: Implement CI/CD pipeline for RAG'" -ForegroundColor White
    Write-Host "   git push origin main" -ForegroundColor White
    exit 1
}

# Check if we're in a git repository
try {
    if ($gitExe -eq "git") {
        $gitDir = & git rev-parse --git-dir 2>&1
    } else {
        $gitDir = & $gitExe rev-parse --git-dir 2>&1
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Not a git repository"
    }
} catch {
    Write-Host "❌ Not a git repository. Please run from repository root." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📋 Checking git status..." -ForegroundColor Yellow

# Show status
if ($gitExe -eq "git") {
    & git status --short
} else {
    & $gitExe status --short
}

Write-Host ""
$confirm = Read-Host "Do you want to proceed with: add, commit, and push? (y/n)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "📦 Adding all changes..." -ForegroundColor Yellow
if ($gitExe -eq "git") {
    & git add .
} else {
    & $gitExe add .
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ git add failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Changes staged" -ForegroundColor Green

Write-Host ""
Write-Host "💾 Committing changes..." -ForegroundColor Yellow

$commitMessage = @"
feat: Implement comprehensive CI/CD pipeline for RAG component

- Add 6-job CI pipeline with Docker-first approach
- Implement pre-commit hooks (black, flake8)
- Reorganize tests into unit/integration/system
- Add system tests with real HTTP requests
- Add concurrency control, permissions, timeouts
- Add Docker image verification
- Add optional Slack notifications
- Add docker-shell.sh helper script
- Based on cheese-app-ci-cd best practices

Fulfills Milestone 4: Continuous Integration and Testing
"@

if ($gitExe -eq "git") {
    & git commit -m $commitMessage
} else {
    & $gitExe commit -m $commitMessage
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ git commit failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Changes committed" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow

# Get current branch
if ($gitExe -eq "git") {
    $branch = & git branch --show-current
} else {
    $branch = & $gitExe branch --show-current
}

if ($LASTEXITCODE -ne 0) {
    $branch = "main"  # Default
}

Write-Host "Pushing to branch: $branch" -ForegroundColor Cyan

if ($gitExe -eq "git") {
    & git push origin $branch
} else {
    & $gitExe push origin $branch
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  ✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📊 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Go to your GitHub repository" -ForegroundColor White
    Write-Host "   2. Click 'Actions' tab" -ForegroundColor White
    Write-Host "   3. Look for 'RAG CI Pipeline' workflow" -ForegroundColor White
    Write-Host "   4. Monitor the CI run (takes ~10-15 minutes)" -ForegroundColor White
    Write-Host ""
    Write-Host "The CI will run:" -ForegroundColor Cyan
    Write-Host "   • Build Docker image" -ForegroundColor White
    Write-Host "   • Lint and format check" -ForegroundColor White
    Write-Host "   • Unit tests" -ForegroundColor White
    Write-Host "   • Integration tests" -ForegroundColor White
    Write-Host "   • System tests (starts RAG server)" -ForegroundColor White
    Write-Host "   • Test summary" -ForegroundColor White
} else {
    Write-Host "❌ git push failed" -ForegroundColor Red
    Write-Host "You may need to:" -ForegroundColor Yellow
    Write-Host "   - Set up remote: git remote add origin <url>" -ForegroundColor White
    Write-Host "   - Authenticate with GitHub" -ForegroundColor White
    exit 1
}

