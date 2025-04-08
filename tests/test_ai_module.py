import sqlite3
import pytest
from unittest.mock import MagicMock, patch

# Import functions to test from your ai_module
from ai_module import get_schema_info, generate_sql_from_prompt, run_ai_query

# Create an in-memory SQLite DB for testing purposes
@pytest.fixture
def in_memory_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    # Create dummy tables for testing that mirror your CSV uploads
    cursor.execute("CREATE TABLE customers (customer_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_name TEXT, location TEXT);")
    cursor.execute("CREATE TABLE products_db (product_id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT, category TEXT, price REAL);")
    # Insert sample data
    cursor.execute("INSERT INTO customers (customer_name, location) VALUES ('Marvel', 'Boston');")
    cursor.execute("INSERT INTO products_db (product_name, category, price) VALUES ('Widget A', 'Gadgets', 19.99);")
    conn.commit()
    yield conn
    conn.close()

def test_get_schema_info(in_memory_db):
    # Get the schema information from the test DB and check that it includes our tables
    schema_info = get_schema_info(in_memory_db)
    assert "customers" in schema_info
    assert "products_db" in schema_info

@patch('ai_module.client.chat.completions.create')
def test_generate_sql_from_prompt(mock_create, in_memory_db):
    # Setup a fake response from the OpenAI client
    fake_response = MagicMock()
    fake_choice = MagicMock()
    # Sample SQL that our fake API returns
    fake_choice.message.content = "SELECT * FROM customers;"
    fake_response.choices = [fake_choice]
    mock_create.return_value = fake_response

    schema_info = get_schema_info(in_memory_db)
    prompt = "Give me all customers"
    sql_query = generate_sql_from_prompt(prompt, schema_info)
    assert sql_query == "SELECT * FROM customers;"

@patch('ai_module.client.chat.completions.create')
def test_run_ai_query(mock_create, in_memory_db, capsys):
    # Setup a fake OpenAI response to simulate a query generation
    fake_response = MagicMock()
    fake_choice = MagicMock()
    fake_choice.message.content = "SELECT c.customer_name, p.product_name FROM customers c JOIN products_db p ON c.customer_id = 1;"
    fake_response.choices = [fake_choice]
    mock_create.return_value = fake_response

    run_ai_query(in_memory_db, "assign customer Marvel to product Widget A")
    captured = capsys.readouterr().out
    # Check that the output includes the generated SQL
    assert "AI-Generated SQL:" in captured
    assert "SELECT" in captured
