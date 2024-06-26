
import pyodbc

# Define your connection parameters
server = 'tcp:maldb.database.windows.net,1433'       # e.g., 'localhost\\SQLEXPRESS' or '192.168.1.1'
database = 'MAL SQL'   # e.g., 'testdb'
username = 'maldb-admin'        # e.g., 'sa'
password = 'Mal@rocks'        # e.g., 'your_password'
driver = '{ODBC Driver 17 for SQL Server}' # Ensure this matches the installed driver
# driver = '/opt/homebrew/lib/libmsodbcsql.17.dylib'
# Define your connection string
connection_string = f"Driver={driver};Server={server};Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

try:
    # Establish a connection
    conn = pyodbc.connect(connection_string)
    print("Connection successful!")

    # Create a cursor from the connection
    cursor = conn.cursor()

    # Execute a query
    cursor.execute('SELECT 1')  # Replace 'your_table' with your table name

    # Fetch the results
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Close the cursor and the connection
    cursor.close()
    conn.close()

except pyodbc.Error as ex:
    sqlstate = ex.args[1]
    print(f"Connection failed: {sqlstate}")
