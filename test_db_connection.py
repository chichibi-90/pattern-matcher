"""
Database Connection Test Script
Tests connection to SQL Server using various authentication methods
"""
import pyodbc
import sys
import os

def get_available_drivers():
    """Get list of available ODBC drivers"""
    drivers = pyodbc.drivers()
    return drivers

def test_connection_with_windows_auth(server, database):
    """Test connection using Windows Authentication (Integrated Security)"""
    print("\n" + "="*60)
    print("Testing Windows Authentication (Integrated Security)")
    print("="*60)
    
    drivers = [
        "ODBC Driver 17 for SQL Server",
        "ODBC Driver 18 for SQL Server",
        "ODBC Driver 13 for SQL Server",
        "SQL Server Native Client 11.0",
        "SQL Server"
    ]
    
    available_drivers = get_available_drivers()
    print(f"\nAvailable ODBC drivers: {', '.join(available_drivers)}")
    
    for driver in drivers:
        if driver not in available_drivers:
            print(f"\n⚠️  Driver '{driver}' not found, skipping...")
            continue
            
        print(f"\n🔍 Trying driver: {driver}")
        try:
            # Windows Authentication connection string
            connection_string = (
                f"DRIVER={{{driver}}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"Trusted_Connection=yes;"
            )
            
            print(f"   Connection string: DRIVER={{{driver}}}; SERVER={server}; DATABASE={database}; Trusted_Connection=yes;")
            
            conn = pyodbc.connect(connection_string, timeout=5)
            print(f"   ✅ SUCCESS! Connected using {driver}")
            
            # Test a simple query
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print(f"   📊 SQL Server Version: {version.split(chr(10))[0]}")
            
            cursor.execute("SELECT DB_NAME()")
            db_name = cursor.fetchone()[0]
            print(f"   📊 Current Database: {db_name}")
            
            cursor.execute("SELECT SYSTEM_USER")
            current_user = cursor.fetchone()[0]
            print(f"   👤 Connected as: {current_user}")
            
            # List databases
            cursor.execute("SELECT name FROM sys.databases ORDER BY name")
            databases = [row[0] for row in cursor.fetchall()]
            print(f"   📁 Available databases ({len(databases)}): {', '.join(databases[:10])}{'...' if len(databases) > 10 else ''}")
            
            # Check for price_data tables
            cursor.execute("""
                SELECT TABLE_SCHEMA, TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME LIKE '%_price_data'
                ORDER BY TABLE_NAME
            """)
            tables = cursor.fetchall()
            if tables:
                print(f"   📊 Found {len(tables)} price_data tables:")
                for schema, table in tables[:5]:
                    print(f"      - {schema}.{table}")
                if len(tables) > 5:
                    print(f"      ... and {len(tables) - 5} more")
            else:
                print(f"   ⚠️  No tables matching pattern '*_price_data' found")
            
            cursor.close()
            conn.close()
            return True
            
        except pyodbc.Error as e:
            print(f"   ❌ Failed: {str(e)}")
            continue
        except Exception as e:
            print(f"   ❌ Unexpected error: {str(e)}")
            continue
    
    return False

def test_connection_with_sql_auth(server, database, username, password):
    """Test connection using SQL Server Authentication"""
    print("\n" + "="*60)
    print("Testing SQL Server Authentication")
    print("="*60)
    
    drivers = [
        "ODBC Driver 17 for SQL Server",
        "ODBC Driver 18 for SQL Server",
        "ODBC Driver 13 for SQL Server",
        "SQL Server"
    ]
    
    available_drivers = get_available_drivers()
    
    for driver in drivers:
        if driver not in available_drivers:
            print(f"\n⚠️  Driver '{driver}' not found, skipping...")
            continue
            
        print(f"\n🔍 Trying driver: {driver}")
        try:
            connection_string = (
                f"DRIVER={{{driver}}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password}"
            )
            
            conn = pyodbc.connect(connection_string, timeout=5)
            print(f"   ✅ SUCCESS! Connected using {driver}")
            
            cursor = conn.cursor()
            cursor.execute("SELECT SYSTEM_USER")
            current_user = cursor.fetchone()[0]
            print(f"   👤 Connected as: {current_user}")
            
            cursor.close()
            conn.close()
            return True
            
        except pyodbc.Error as e:
            print(f"   ❌ Failed: {str(e)}")
            continue
        except Exception as e:
            print(f"   ❌ Unexpected error: {str(e)}")
            continue
    
    return False

def main():
    print("="*60)
    print("SQL Server Connection Test")
    print("="*60)
    
    # Get configuration
    server = os.getenv('DB_SERVER', 'localhost')
    database = os.getenv('DB_DATABASE', 'price_history')
    username = os.getenv('DB_USERNAME', 'sa')
    password = os.getenv('DB_PASSWORD', '')
    
    print(f"\nConfiguration:")
    print(f"  Server: {server}")
    print(f"  Database: {database}")
    print(f"  Username: {username if username else '(not set)'}")
    print(f"  Password: {'*' * len(password) if password else '(not set)'}")
    print(f"  Current Windows User: {os.getenv('USERNAME', 'unknown')}")
    
    # First try Windows Authentication (most likely to work for localhost)
    success = test_connection_with_windows_auth(server, database)
    
    # If Windows auth fails and SQL auth credentials are provided, try SQL auth
    if not success and username and password and password != 'your_password_here':
        success = test_connection_with_sql_auth(server, database, username, password)
    
    print("\n" + "="*60)
    if success:
        print("✅ CONNECTION TEST PASSED!")
        print("="*60)
        return 0
    else:
        print("❌ CONNECTION TEST FAILED!")
        print("="*60)
        print("\nTroubleshooting tips:")
        print("1. Verify SQL Server is running (check Services)")
        print("2. Verify SQL Server Browser service is running (for named instances)")
        print("3. Check Windows Firewall settings")
        print("4. Try 'localhost' or 'localhost\\SQLEXPRESS' for named instances")
        print("5. Verify the database name exists")
        print("6. For Windows Auth: Ensure your Windows user has SQL Server access")
        print("7. For SQL Auth: Verify username and password are correct")
        return 1

if __name__ == '__main__':
    sys.exit(main())


