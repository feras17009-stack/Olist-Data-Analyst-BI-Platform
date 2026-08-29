"""
Database management module for PostgreSQL and SQLite.
Handles connection pooling, DDL execution, data ingestion, and analytical querying.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.config import (
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, SQLITE_DB_PATH, SQL_DIR
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_postgres_engine() -> Optional[Engine]:
    """
    Create a PostgreSQL SQLAlchemy Engine if available.
    """
    url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    try:
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info(f"Connected to PostgreSQL database '{DB_NAME}' at {DB_HOST}:{DB_PORT}")
        return engine
    except Exception as e:
        logger.warning(f"PostgreSQL connection failed: {e}. Falling back to SQLite.")
        return None


def get_sqlite_engine(db_path: Optional[Path] = None) -> Engine:
    """
    Create an SQLite SQLAlchemy Engine for local execution.
    """
    path = db_path or SQLITE_DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{path}")
    logger.info(f"Connected to SQLite database at {path}")
    return engine


def get_database_engine(prefer_postgres: bool = True) -> Tuple[Engine, str]:
    """
    Get active database engine (PostgreSQL if reachable, otherwise SQLite).
    """
    if prefer_postgres:
        pg = get_postgres_engine()
        if pg is not None:
            return pg, "postgres"
            
    sqlite_eng = get_sqlite_engine()
    return sqlite_eng, "sqlite"


def execute_sql_file(engine: Engine, sql_file_path: Path) -> None:
    """
    Read and execute SQL statements from a file.
    """
    if not sql_file_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")
        
    logger.info(f"Executing SQL file: {sql_file_path.name}...")
    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()
        
    # Split queries by semicolon, handling comments
    queries = [q.strip() for q in sql_content.split(";") if q.strip()]
    with engine.begin() as conn:
        for q in queries:
            if q:
                conn.execute(text(q))
    logger.info(f"Successfully executed {len(queries)} queries from {sql_file_path.name}")


def load_dataframe_to_table(
    df: pd.DataFrame, 
    table_name: str, 
    engine: Engine, 
    schema: Optional[str] = None,
    if_exists: str = "replace",
    chunksize: int = 10000
) -> None:
    """
    Load a Pandas DataFrame into a database table.
    """
    logger.info(f"Loading {len(df):,} rows into table '{table_name}' (schema: {schema})...")
    # For SQLite, avoid schema prefix in to_sql if schema not attached, or use prefix table name
    if engine.dialect.name == "sqlite" and schema:
        actual_table_name = f"{schema}_{table_name}"
        actual_schema = None
    else:
        actual_table_name = table_name
        actual_schema = schema
        
    df.to_sql(
        name=actual_table_name,
        con=engine,
        schema=actual_schema,
        if_exists=if_exists,
        index=False,
        chunksize=chunksize
    )
    logger.info(f"Successfully loaded '{actual_table_name}'.")


def run_query(query: str, engine: Engine) -> pd.DataFrame:
    """
    Run an arbitrary SQL query and return a DataFrame.
    """
    with engine.connect() as conn:
        result_df = pd.read_sql_query(text(query), conn)
    return result_df
