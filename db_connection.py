import pyodbc
from config import DB_CONFIG
from datetime import datetime, timedelta

def get_db_connection():
    """Create and return a database connection"""
    # Try different ODBC driver versions
    drivers = [
        "ODBC Driver 17 for SQL Server",
        "ODBC Driver 18 for SQL Server",
        "ODBC Driver 13 for SQL Server",
        "SQL Server"
    ]
    
    # Determine authentication method
    # Use Windows Authentication if no username/password provided or password is placeholder
    use_windows_auth = (
        not DB_CONFIG.get('username') or 
        not DB_CONFIG.get('password') or 
        DB_CONFIG.get('password') == 'your_password_here'
    )
    
    for driver in drivers:
        try:
            if use_windows_auth:
                # Windows Authentication (Integrated Security)
                connection_string = (
                    f"DRIVER={{{driver}}};"
                    f"SERVER={DB_CONFIG['server']};"
                    f"DATABASE={DB_CONFIG['database']};"
                    f"Trusted_Connection=yes;"
                )
            else:
                # SQL Server Authentication
                connection_string = (
                    f"DRIVER={{{driver}}};"
                    f"SERVER={DB_CONFIG['server']};"
                    f"DATABASE={DB_CONFIG['database']};"
                    f"UID={DB_CONFIG['username']};"
                    f"PWD={DB_CONFIG['password']}"
                )
            return pyodbc.connect(connection_string)
        except pyodbc.Error:
            continue
    
    # If all drivers fail, raise an error
    auth_method = "Windows Authentication" if use_windows_auth else "SQL Server Authentication"
    raise Exception(f"Could not connect to database using {auth_method}. Tried drivers: {', '.join(drivers)}")

def get_ccy_pairs():
    """
    Query the database to find all tables matching the pattern *_price_data
    and extract the CCY pair names
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query to get all tables ending with _price_data
    query = """
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE = 'BASE TABLE' 
    AND TABLE_NAME LIKE '%_price_data'
    ORDER BY TABLE_NAME
    """
    
    cursor.execute(query)
    tables = cursor.fetchall()
    
    # Extract CCY pair names (e.g., 'NZDCAD_price_data' -> 'NZDCAD')
    pairs = []
    for table in tables:
        table_name = table[0]
        # Remove '_price_data' suffix to get the CCY pair
        ccy_pair = table_name.replace('_price_data', '')
        pairs.append({
            'name': ccy_pair,
            'table_name': table_name
        })
    
    cursor.close()
    conn.close()
    
    return pairs

def get_price_data(ccy_pair, date=None):
    """
    Get price data for a specific currency pair
    If date is not provided, get the most recent day's data
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    table_name = f"{ccy_pair}_price_data"
    
    # If no date specified, get the most recent day's data
    if date is None:
        # Get the most recent date in the table
        query = f"SELECT TOP 1 [date] FROM [{table_name}] ORDER BY [date] DESC"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            # Extract date part (format: '2021.01.03 22:39:00')
            most_recent_date = result[0]
            # Get just the date part (before the space)
            date_str = most_recent_date.split(' ')[0] if ' ' in most_recent_date else most_recent_date
            # Query for all data on that day
            query = f"""
            SELECT [date], [open], [high], [low], [close], [volume]
            FROM [{table_name}]
            WHERE [date] LIKE '{date_str}%'
            ORDER BY [date]
            """
        else:
            cursor.close()
            conn.close()
            return []
    else:
        # Query for specific date
        query = f"""
        SELECT [date], [open], [high], [low], [close], [volume]
        FROM [{table_name}]
        WHERE [date] LIKE '{date}%'
        ORDER BY [date]
        """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Format data for frontend
    data = []
    for row in rows:
        data.append({
            'date': row[0],
            'open': float(row[1]),
            'high': float(row[2]),
            'low': float(row[3]),
            'close': float(row[4]),
            'volume': int(row[5])
        })
    
    cursor.close()
    conn.close()
    
    return data

def find_similar_patterns(source_ccy_pair, source_data, num_candles=20, top_n=5):
    """
    Find similar price patterns in other currency pairs
    
    Args:
        source_ccy_pair: The currency pair to match against
        source_data: The price data for the source currency pair
        num_candles: Number of recent candles to use for pattern matching
        top_n: Number of similar patterns to return
    
    Returns:
        List of dictionaries with similar patterns and their similarity scores
    """
    if len(source_data) < num_candles:
        num_candles = len(source_data)
    
    # Extract the pattern from source data (normalized closing prices)
    source_pattern = source_data[-num_candles:]
    source_closes = [d['close'] for d in source_pattern]
    
    # Normalize the pattern (0-1 scale)
    min_close = min(source_closes)
    max_close = max(source_closes)
    if max_close == min_close:
        normalized_source = [0.5] * len(source_closes)
    else:
        normalized_source = [(c - min_close) / (max_close - min_close) for c in source_closes]
    
    # Get all currency pairs
    all_pairs = get_ccy_pairs()
    
    # Compare with other currency pairs
    similarities = []
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for pair in all_pairs:
        if pair['name'] == source_ccy_pair:
            continue  # Skip the source pair itself
        
        try:
            # Get price data for this pair
            pair_data = get_price_data(pair['name'])
            
            if len(pair_data) < num_candles:
                continue
            
            # Extract pattern from this pair
            pair_pattern = pair_data[-num_candles:]
            pair_closes = [d['close'] for d in pair_pattern]
            
            # Normalize this pattern
            min_pair = min(pair_closes)
            max_pair = max(pair_closes)
            if max_pair == min_pair:
                normalized_pair = [0.5] * len(pair_closes)
            else:
                normalized_pair = [(c - min_pair) / (max_pair - min_pair) for c in pair_closes]
            
            # Calculate similarity using correlation coefficient
            similarity = calculate_correlation(normalized_source, normalized_pair)
            
            similarities.append({
                'ccy_pair': pair['name'],
                'similarity': similarity,
                'data': pair_data[-num_candles:]  # Return the matching pattern data
            })
        except Exception:
            # Skip pairs that can't be processed
            continue
    
    cursor.close()
    conn.close()
    
    # Sort by similarity (highest first) and return top N
    similarities.sort(key=lambda x: x['similarity'], reverse=True)
    return similarities[:top_n]

def calculate_correlation(pattern1, pattern2):
    """
    Calculate Pearson correlation coefficient between two patterns
    Returns a value between -1 and 1, where 1 is perfect positive correlation
    """
    if len(pattern1) != len(pattern2):
        return 0
    
    n = len(pattern1)
    mean1 = sum(pattern1) / n
    mean2 = sum(pattern2) / n
    
    numerator = sum((pattern1[i] - mean1) * (pattern2[i] - mean2) for i in range(n))
    sum_sq1 = sum((pattern1[i] - mean1) ** 2 for i in range(n))
    sum_sq2 = sum((pattern2[i] - mean2) ** 2 for i in range(n))
    
    denominator = (sum_sq1 * sum_sq2) ** 0.5
    
    if denominator == 0:
        return 0
    
    correlation = numerator / denominator
    return correlation

