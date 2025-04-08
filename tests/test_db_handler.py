import sqlite3
import pytest
from db_handler import connect_db, list_tables, run_sql_query

@pytest.fixture
def in_memory_db():
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()

def test_connect_db():
    # Test that connecting to an in-memory database returns a valid connection
    conn = connect_db(":memory:")
    assert conn is not None
    conn.close()

def test_list_tables(in_memory_db, capsys):
    # Create a test table
    cursor = in_memory_db.cursor()
    cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT);")
    in_memory_db.commit()
    list_tables(in_memory_db)
    captured = capsys.readouterr().out
    assert "test" in captured

def test_run_sql_query(in_memory_db, capsys):
    # Create a table and insert some data, then verify the query returns expected result
    cursor = in_memory_db.cursor()
    cursor.execute("CREATE TABLE sample (id INTEGER PRIMARY KEY, value TEXT);")
    cursor.execute("INSERT INTO sample (value) VALUES ('Hello world');")
    in_memory_db.commit()
    run_sql_query(in_memory_db, "SELECT * FROM sample;")
    captured = capsys.readouterr().out
    assert "Hello world" in captured
