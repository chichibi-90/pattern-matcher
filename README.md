# Currency Pair Price Data Viewer

A Python-based web application for viewing intraday price data from SQL Server database with interactive candlestick charts.

## Features

- Automatically discovers all currency pair tables in the database
- Interactive candlestick chart visualization using Plotly
- Displays a day's worth of intraday price data
- Modern, responsive web UI

## Prerequisites

- Python 3.7 or higher
- SQL Server with price_history database
- ODBC Driver 17 for SQL Server (or compatible version)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure database connection in `config.py` or set environment variables:
   - `DB_SERVER`: SQL Server hostname/address
   - `DB_DATABASE`: Database name (default: price_history)
   - `DB_USERNAME`: SQL Server username
   - `DB_PASSWORD`: SQL Server password

## Usage

1. Update the database configuration in `config.py` with your SQL Server credentials.

2. Run the application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

4. Select a currency pair from the dropdown to view its intraday candlestick chart.

## Database Schema

The application expects tables with the naming pattern `{CCY_PAIR}_price_data` (e.g., `NZDCAD_price_data`) with the following columns:
- `date` (varchar): Date and time of the price data
- `open` (float): Opening price
- `high` (float): Highest price
- `low` (float): Lowest price
- `close` (float): Closing price
- `volume` (bigint): Trading volume

## Notes

- The application automatically queries for the most recent day's data when a currency pair is selected
- If no data is found, an appropriate message will be displayed
- The chart includes both candlestick price data and volume bars


