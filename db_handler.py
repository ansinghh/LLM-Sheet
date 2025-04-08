import sqlite3
from csv_loader import create_table_from_csv
from utils import log_error

def connect_db(db_path="mydatabase.db"):
    return sqlite3.connect(db_path)

def get_existing_schema(table_name, conn):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns_info = cursor.fetchall()
    return {col[1]: col[2] for col in columns_info}

def create_table_with_conflict_check(csv_path, table_name, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    exists = cursor.fetchone()

    if exists:
        existing_schema = get_existing_schema(table_name, conn)
        print(f"Table '{table_name}' already exists with schema: {existing_schema}")
        action = input("Conflict! Overwrite (O), Rename (R), or Skip (S)? ").strip().upper()

        if action == "O":
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            conn.commit()
            print(f"Table '{table_name}' dropped. Recreating table.")
        elif action == "R":
            new_table_name = table_name + "_new"
            print(f"Creating table as '{new_table_name}' instead.")
            table_name = new_table_name
        elif action == "S":
            print("Skipping table creation.")
            return
        else:
            log_error(f"Invalid user action for table {table_name}. Action: {action}")
            print("Invalid action. Aborting table creation.")
            return

    create_table_from_csv(csv_path, table_name, conn)
    print(f"Table '{table_name}' created successfully.")

def list_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if tables:
        print("Tables in the database:")
        for t in tables:
            print(" -", t[0])
    else:
        print("No tables found in the database.")

def run_sql_query(conn, query):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            for row in results:
                print(row)
        else:
            print("Query executed successfully. No rows returned.")
    except Exception as e:
        print(f"Error running query: {e}")
