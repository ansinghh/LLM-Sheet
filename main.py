from dotenv import load_dotenv
load_dotenv()  # Ensure environment variables are loaded

import os
from db_handler import connect_db, create_table_with_conflict_check, list_tables, run_sql_query
from ai_module import run_ai_query

def print_help():
    help_text = """
Available Commands:
  upload csv     - List available CSV files and upload one to the database.
  query          - Enter an SQL query to view data in the database.
  ai query       - Enter a natural language query to generate and execute an SQL command.
  list tables    - List all tables in the database.
  help           - Show this help message.
  exit / quit    - Exit the application.
"""
    print(help_text)

def list_csv_files():
    """
    List all CSV files in the current directory.
    """
    csv_files = [f for f in os.listdir('.') if f.lower().endswith('.csv')]
    if csv_files:
        print("Available CSV files:")
        for idx, f in enumerate(csv_files, start=1):
            print(f" {idx}. {f}")
    else:
        print("No CSV files found in the current directory.")
    return csv_files

def cli_loop():
    db_path = "mydatabase.db"
    conn = connect_db(db_path)
    print("Welcome to the SQLite CLI with AI assistance. Type 'help' for options.")
    
    while True:
        command = input("Command> ").strip().lower()
        
        if command in ['exit', 'quit']:
            print("Exiting...")
            break
        
        elif command == 'upload csv':
            csv_files = list_csv_files()
            if csv_files:
                file_choice = input("Enter the CSV file name (or number) you want to upload: ").strip()
                if file_choice.isdigit():
                    idx = int(file_choice) - 1
                    if 0 <= idx < len(csv_files):
                        csv_file = csv_files[idx]
                    else:
                        print("Invalid selection.")
                        continue
                else:
                    csv_file = file_choice
                    if csv_file not in csv_files:
                        print("File not found.")
                        continue
                table_name = input("Enter the table name for this CSV file: ").strip()
                create_table_with_conflict_check(csv_file, table_name, conn)
            else:
                print("No CSV files available to upload.")
        
        elif command == 'query':
            query = input("Enter your SQL query: ").strip()
            run_sql_query(conn, query)
        
        elif command == 'ai query':
            prompt = input("Enter your natural language query: ").strip()
            run_ai_query(conn, prompt)
        
        elif command == 'list tables':
            list_tables(conn)
        
        elif command == 'help':
            print_help()
        
        else:
            print("Unknown command. Type 'help' for available options.")
    
    conn.close()

if __name__ == "__main__":
    cli_loop()
