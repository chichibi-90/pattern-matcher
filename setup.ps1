# Currency Pair Price Data Viewer - Setup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Currency Pair Price Data Viewer - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Try to find Python
$pythonPath = $null

# First, try python command (if in PATH)
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $pythonPath = "python"
        Write-Host "Python found: $pythonVersion" -ForegroundColor Green
    }
} catch {
    # Python not in PATH, try common locations
}

# If not found, try common installation paths
if (-not $pythonPath) {
    $commonPaths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe",
        "$env:ProgramFiles\Python*\python.exe",
        "C:\Python*\python.exe"
    )
    
    foreach ($pathPattern in $commonPaths) {
        $found = Get-ChildItem $pathPattern -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) {
            $pythonPath = $found.FullName
            $version = & $found.FullName --version 2>&1
            Write-Host "Python found at: $pythonPath" -ForegroundColor Green
            Write-Host "Version: $version" -ForegroundColor Green
            break
        }
    }
}

if (-not $pythonPath) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing required packages..." -ForegroundColor Yellow
& $pythonPath -m pip install --upgrade pip
& $pythonPath -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update config.py with your database credentials" -ForegroundColor Yellow
Write-Host "2. Run start.bat or start.ps1 to start the application" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"

