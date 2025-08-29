"""
DuckDB-Datenablage & Abfragefunktionen.
"""
# src/data_store.py
from __future__ import annotations
import os
import duckdb
import pandas as pd

DEFAULT_DB = "data/tripadvisor.duckdb"
DEFAULT_TABLE = "reviews"

def connect(db_path: str = DEFAULT_DB) -> duckdb.DuckDBPyConnection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return duckdb.connect(db_path)

def bootstrap_from_csv(csv_path: str, db_path: str = DEFAULT_DB, table: str = DEFAULT_TABLE,
                       overwrite: bool = False, make_parquet: bool = True) -> None:
    con = connect(db_path)
    if overwrite:
        con.execute(f"DROP TABLE IF EXISTS {table};")
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} AS
        SELECT * FROM read_csv_auto(?, HEADER=TRUE);
    """, [csv_path])
    # Deduplizieren
    con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT DISTINCT * FROM {table};")
    if make_parquet:
        con.execute(f"COPY (SELECT * FROM {table}) TO 'data/reviews.parquet' (FORMAT PARQUET);")

def query_df(sql: str, db_path: str = DEFAULT_DB, params: list | None = None) -> pd.DataFrame:
    con = connect(db_path)
    return con.execute(sql, params or []).df()

def get_text_and_rating(db_path: str = DEFAULT_DB, table: str = DEFAULT_TABLE) -> pd.DataFrame:
    # Spalten heuristisch erkennen
    info = query_df(f"PRAGMA table_info({table});", db_path)
    cols = {row['name'].lower(): row['name'] for _, row in info.iterrows()}
    text_col = next((cols[c] for c in ['review','text','content','review_text','reviews'] if c in cols), None)
    rating_col = next((cols[c] for c in ['rating','score','stars','star_rating'] if c in cols), None)
    if not text_col:
        sample = query_df(f"SELECT * FROM {table} LIMIT 1;", db_path)
        text_col = sample.columns[0]
    sel = [text_col] + ([rating_col] if rating_col else [])
    q = f"SELECT {', '.join(sel)} FROM {table} WHERE {text_col} IS NOT NULL;"
    return query_df(q, db_path)
