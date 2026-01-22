#!/usr/bin/env python3
"""
Script to fix the alembic version table.
"""
from sqlalchemy import create_engine, text
from src.config.settings import settings

def fix_alembic_version():
    # Use sync engine to update the database
    sync_url = settings.database_url.replace("asyncpg", "psycopg2")
    engine = create_engine(sync_url)

    # Update the alembic version to match the actual migration file
    # The actual migration file is 082ad38b8094_initial_todo_model_with_user_id.py
    with engine.connect() as conn:
        # Begin a transaction
        trans = conn.begin()

        # Update the alembic version
        conn.execute(text("UPDATE alembic_version SET version_num = '082ad38b8094' WHERE version_num = '001'"))

        trans.commit()
        print("Alembic version updated successfully!")

if __name__ == "__main__":
    fix_alembic_version()