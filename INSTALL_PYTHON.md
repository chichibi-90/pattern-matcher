# How to Install Python on Windows

## Method 1: Official Python Website (Recommended)

### Step 1: Download Python
1. Go to **https://www.python.org/downloads/**
2. Click the big yellow "Download Python" button (it will download the latest version)
   - Or scroll down to find a specific version if needed

### Step 2: Run the Installer
1. Open the downloaded `.exe` file (usually in your Downloads folder)
2. **IMPORTANT**: Check the box that says **"Add Python to PATH"** at the bottom of the installer
   - This is crucial! It allows you to use `python` from the command line
3. Click "Install Now" (or "Customize installation" if you want to change options)
4. Wait for installation to complete

### Step 3: Verify Installation
1. Open a new PowerShell or Command Prompt window
2. Type: `python --version`
3. You should see something like: `Python 3.11.x` or `Python 3.12.x`

## Method 2: Microsoft Store (Alternative)

1. Open the **Microsoft Store** app
2. Search for "Python"
3. Click on "Python 3.11" or "Python 3.12" (or latest version)
4. Click "Get" or "Install"
5. The PATH is usually configured automatically with this method

## Method 3: Using winget (Windows Package Manager)

If you have Windows 10/11 with winget installed:

```powershell
winget install Python.Python.3.12
```

## After Installation

1. **Close and reopen** your terminal/PowerShell window (important!)
2. Verify Python is working:
   ```bash
   python --version
   ```
3. Verify pip (Python package manager) is working:
   ```bash
   pip --version
   ```

## Troubleshooting

### "Python is not recognized"
- Make sure you checked "Add Python to PATH" during installation
- If you forgot, you can:
  1. Reinstall Python and check the box this time, OR
  2. Manually add Python to PATH:
     - Search for "Environment Variables" in Windows
     - Edit "Path" variable
     - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python3XX`
     - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python3XX\Scripts`

### Still having issues?
- Restart your computer after installation
- Make sure you're using a new terminal window (not the one that was open during installation)

## Next Steps

Once Python is installed:
1. Run `setup.bat` in this folder to install dependencies
2. Update `config.py` with your database credentials
3. Run `start.bat` to start the application


