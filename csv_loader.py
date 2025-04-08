import pandas as pd

def infer_sqlite_type(pd_series):
    if pd.api.types.is_integer_dtype(pd_series):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(pd_series):
        return "REAL"
    else:
        # Default to TEXT for strings, dates, etc.
        return "TEXT"

def create_table_from_csv(csv_path, table_name, conn):
    df = pd.read_csv(csv_path)
    columns = []
    for col in df.columns:
        col_type = infer_sqlite_type(df[col])
        columns.append(f"[{col}] {col_type}")
        
    create_table_statement = f"CREATE TABLE IF NOT EXISTS [{table_name}] ({', '.join(columns)});"
    
    cursor = conn.cursor()
    cursor.execute(create_table_statement)
    conn.commit()
    
    df.to_sql(table_name, conn, if_exists='append', index=False)
