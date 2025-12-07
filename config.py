import os

# Database configuration
# Update these values to match your SQL Server setup
# You can either:
# 1. Edit the values below directly, OR
# 2. Set environment variables (DB_SERVER, DB_DATABASE, DB_USERNAME, DB_PASSWORD)
#
# Authentication:
# - If username/password are not set or password is 'your_password_here', 
#   Windows Authentication (Integrated Security) will be used
# - To use SQL Server Authentication, set both username and password

DB_CONFIG = {
    'server': os.getenv('DB_SERVER', 'localhost'),  # SQL Server hostname or IP address
    'database': os.getenv('DB_DATABASE', 'price_history'),  # Database name
    'username': os.getenv('DB_USERNAME', ''),  # SQL Server username (leave empty for Windows Auth)
    'password': os.getenv('DB_PASSWORD', '')  # SQL Server password (leave empty for Windows Auth)
}

# Example configurations:
# Local SQL Server: 'server': 'localhost' or 'server': 'localhost\\SQLEXPRESS'
# Remote SQL Server: 'server': '192.168.1.100' or 'server': 'myserver.example.com'
# Named instance: 'server': 'localhost\\INSTANCENAME'

