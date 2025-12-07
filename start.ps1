# Currency Pair Price Data Viewer - Start Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Currency Pair Price Data Viewer" -ForegroundColor Cyan
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
            Write-Host "Python found at: $pythonPath" -ForegroundColor Green
            break
        }
    }
}

if (-not $pythonPath) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if dependencies are installed
try {
    & $pythonPath -c "import flask" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Flask not installed"
    }
} catch {
    Write-Host "ERROR: Flask is not installed" -ForegroundColor Red
    Write-Host "Please run setup.ps1 first to install dependencies" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Starting Flask application..." -ForegroundColor Green
Write-Host ""
Write-Host "The application will be available at: http://localhost:5000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

& $pythonPath app.py

