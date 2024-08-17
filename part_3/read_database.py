import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'localhost',
}

try:
    # Connect to the default 'postgres' database to check if 'mydatabase' exists
    conn = psycopg2.connect(dbname='postgres', user=db_params['user'], password=db_params['password'],
                            host=db_params['host'])
    cur = conn.cursor()

    # Check if the database exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_params['dbname'],))
    exists = cur.fetchone()

    if exists:
        print(f"Database '{db_params['dbname']}' exists!")

        # Connect to 'mydatabase'
        conn.close()  # Close previous connection
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Select the first 5 rows from a specific table (replace 'your_table' with the actual table name)
        cur.execute("SELECT * FROM table_name LIMIT 5")
        rows = cur.fetchall()

        # Print the rows
        for row in rows:
            print(row)
    else:
        print(f"Database '{db_params['dbname']}' does not exist!")

except Exception as e:
    print("An error occurred:", e)

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
