#!/usr/bin/env python3
"""
Script to check current foreign key constraints.
"""
from sqlalchemy import create_engine, text
from src.config.settings import settings

def check_constraints():
    # Use sync engine to inspect the database
    sync_url = settings.database_url.replace("asyncpg", "psycopg2")
    engine = create_engine(sync_url)

    # Check foreign key constraints
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                tc.table_name,
                tc.constraint_name,
                tc.constraint_type,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_name IN ('todo', 'todos');
        """))

        constraints = result.fetchall()
        print("Foreign key constraints for todo/todos tables:")
        for row in constraints:
            print(f"  {row[0]}.{row[2]} -> {row[4]}.{row[5]} (constraint: {row[1]})")

if __name__ == "__main__":
    check_constraints()