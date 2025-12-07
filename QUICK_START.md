# Quick Start Guide

## Prerequisites

1. **Python 3.7 or higher** - Download from [python.org](https://www.python.org/downloads/)
   - ⚠️ **Important**: Check "Add Python to PATH" during installation

2. **SQL Server ODBC Driver** - Usually comes with SQL Server installation
   - If needed, download from Microsoft

## Setup Steps

### Step 1: Install Dependencies

**Option A - Using Batch File (Windows):**
```bash
setup.bat
```

**Option B - Using PowerShell:**
```powershell
.\setup.ps1
```

**Option C - Manual:**
```bash
pip install -r requirements.txt
```

### Step 2: Configure Database Connection

Edit `config.py` and update the database credentials:

```python
DB_CONFIG = {
    'server': 'your_server_name',      # e.g., 'localhost' or 'localhost\\SQLEXPRESS'
    'database': 'price_history',       # Your database name
    'username': 'your_username',       # SQL Server username
    'password': 'your_password'       # SQL Server password
}
```

### Step 3: Start the Application

**Option A - Using Batch File:**
```bash
start.bat
```

**Option B - Using PowerShell:**
```powershell
.\start.ps1
```

**Option C - Manual:**
```bash
python app.py
```

### Step 4: Open in Browser

Navigate to: **http://localhost:5000**

## Troubleshooting

### Python not found
- Make sure Python is installed and added to PATH
- Try restarting your terminal/command prompt after installing Python
- Verify with: `python --version`

### Database connection errors
- Verify SQL Server is running
- Check firewall settings
- Verify credentials in `config.py`
- Ensure ODBC Driver is installed

### Module not found errors
- Run `setup.bat` or `pip install -r requirements.txt` again
- Make sure you're using the correct Python environment

## Database Requirements

Your database should contain tables with the naming pattern: `{CCY_PAIR}_price_data`

Example tables:
- `NZDCAD_price_data`
- `EURUSD_price_data`
- `GBPUSD_price_data`

Each table should have columns: `date`, `open`, `high`, `low`, `close`, `volume`


