#!/usr/bin/env python3
"""
Script to check the current database schema.
"""
import asyncio
from sqlalchemy import create_engine, inspect
from src.config.settings import settings

def check_db_schema():
    # Use sync engine to inspect the database
    sync_url = settings.database_url.replace("asyncpg", "psycopg2")
    engine = create_engine(sync_url)

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables:", tables)

    if 'todo' in tables:
        columns = inspector.get_columns('todo')
        print("\nTodo table columns:")
        for col in columns:
            print(f"  {col['name']}: {col['type']} (nullable: {col['nullable']})")

    if 'alembic_version' in tables:
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM alembic_version"))
            versions = result.fetchall()
            print(f"\nAlembic versions: {versions}")

if __name__ == "__main__":
    check_db_schema()