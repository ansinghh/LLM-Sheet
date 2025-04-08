# from dotenv import load_dotenv
# load_dotenv()  # Load environment variables from .env before other imports that need them

# import os
# from openai import OpenAI

# # Now the API key from the .env file is available
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def get_schema_info(conn):
#     """
#     Generate a summary of the database schema (tables and their columns).
#     """
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     tables = [t[0] for t in cursor.fetchall()]
#     schema_descriptions = []
#     for table in tables:
#         cursor.execute(f"PRAGMA table_info({table});")
#         columns_info = cursor.fetchall()
#         columns_str = ", ".join([f"{col[1]} ({col[2]})" for col in columns_info])
#         schema_descriptions.append(f"Table '{table}': {columns_str}")
#     return "\n".join(schema_descriptions)

# def generate_sql_from_prompt(prompt, schema_info):
#     """
#     Use the OpenAI API to generate a SQLite-compatible SQL query based on the provided
#     schema and a natural language query. The system prompt instructs the LLM to handle
#     everyday language. In particular, if the query is about adding a customer, assume that 
#     the customers table is defined with an auto-incrementing primary key (customer_id) and 
#     generate an INSERT statement that does not include the customer_id column.
#     """
#     messages = [
#         {
#             "role": "system",
#             "content": (
#                 "You are an expert assistant that converts natural language queries into SQLite SQL queries. "
#                 "Users may phrase their queries in everyday conversational language, for example: "
#                 "'Give me all of the customers currently in the system', 'Which customer is in LA?', or "
#                 "'add a customer with name Marvel who lives in Boston'. "
#                 "If the query is about adding a customer, assume that the customers table is defined with an auto-incrementing "
#                 "primary key (customer_id) and generate an INSERT statement that does not include the customer_id column. "
#                 "Output only the SQL query with no extra explanation."
#             )
#         },
#         {
#             "role": "user",
#             "content": f"Database schema:\n{schema_info}\n\nUser request: {prompt}"
#         }
#     ]
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4",  # Change to "gpt-4" if needed
#             messages=messages,
#             temperature=0
#         )
#         sql_query = response.choices[0].message.content.strip()
#         return sql_query
#     except Exception as e:
#         print(f"Error calling OpenAI API: {e}")
#         return None

# def run_ai_query(conn, prompt):
#     """
#     Generate a SQL query from a natural language prompt using the LLM,
#     execute the query, and print the results.
#     """
#     schema_info = get_schema_info(conn)
#     sql_query = generate_sql_from_prompt(prompt, schema_info)
#     if not sql_query:
#         print("Failed to generate SQL query.")
#         return

#     print("AI-Generated SQL:")
#     print(sql_query)
#     cursor = conn.cursor()
#     try:
#         cursor.execute(sql_query)
#         results = cursor.fetchall()
#         if results:
#             print("Query Results:")
#             for row in results:
#                 print(row)
#         else:
#             print("Query executed successfully. No rows returned.")
#     except Exception as e:
#         print("Error executing SQL query:", e)


from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env before other imports that need them

import os
from openai import OpenAI

# Now the API key from the .env file is available
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_schema_info(conn):
    """
    Generate a summary of the database schema (tables and their columns).
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    schema_descriptions = []
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns_info = cursor.fetchall()
        columns_str = ", ".join([f"{col[1]} ({col[2]})" for col in columns_info])
        schema_descriptions.append(f"Table '{table}': {columns_str}")
    return "\n".join(schema_descriptions)

def generate_sql_from_prompt(prompt, schema_info):
    """
    Use the OpenAI API to generate a SQLite-compatible SQL query based on the provided
    schema and a natural language query.

    The system prompt instructs the LLM to handle everyday language with arbitrary CSV schemas.
    In particular, if the query is about assigning or relating entities from two CSV files
    (for example, "assign customer Marvel to product Widget A"), generate a SQL query that joins
    the relevant tables dynamically (using common columns such as customer_name or product_name)
    even if no explicit relationship table exists.
    
    For queries about adding a customer, assume that the customers table is defined with an auto-incrementing
    primary key (customer_id) and generate an INSERT statement that omits that column.

    Output only the SQL query with no extra explanation.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert assistant that converts natural language queries into SQLite SQL queries. "
                "Users can upload arbitrary CSV files, so the database schema may vary. Handle the queries in everyday conversational language. "
                "For example, users might say 'Give me all of the customers currently in the system', 'Which customer is in LA?', "
                "or 'assign customer Marvel to product Widget A'. "
                "For queries about adding a customer, assume the customers table has an auto-incrementing primary key (customer_id) and generate an INSERT statement without specifying that column. "
                "For assignment or relational queries, if there is no pre-defined join table, generate a SQL query that uses subqueries or JOINs to relate data from the appropriate tables using common columns (like customer_name and product_name). "
                "Output only the SQL query with no extra explanation."
            )
        },
        {
            "role": "user",
            "content": f"Database schema:\n{schema_info}\n\nUser request: {prompt}"
        }
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Using GPT-4 for improved accuracy and coding logic
            messages=messages,
            temperature=0
        )
        sql_query = response.choices[0].message.content.strip()
        return sql_query
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

def run_ai_query(conn, prompt):
    """
    Generate a SQL query from a natural language prompt using the LLM,
    execute the query, and print the results.
    """
    schema_info = get_schema_info(conn)
    sql_query = generate_sql_from_prompt(prompt, schema_info)
    if not sql_query:
        print("Failed to generate SQL query.")
        return

    print("AI-Generated SQL:")
    print(sql_query)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        if results:
            print("Query Results:")
            for row in results:
                print(row)
        else:
            print("Query executed successfully. No rows returned.")
    except Exception as e:
        print("Error executing SQL query:", e)
