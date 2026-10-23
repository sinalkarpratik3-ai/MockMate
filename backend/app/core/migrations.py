"""
Database Schema Migration for MockMate

Safely and idempotently migrates PostgreSQL datetime columns from
TIMESTAMP WITHOUT TIME ZONE to TIMESTAMP WITH TIME ZONE.

Preserves existing records by interpreting naive timestamps as UTC.
Compatible with fresh AWS RDS deployments and existing PostgreSQL databases.
"""

import asyncio
import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

logger = logging.getLogger("uvicorn.error")

# All application tables and columns that store datetime timestamps
TIMESTAMP_COLUMNS = [
    ("users", "created_at"),
    ("users", "updated_at"),
    ("interviews", "created_at"),
    ("interviews", "completed_at"),
    ("questions", "created_at"),
    ("answers", "evaluated_at"),
    ("bookmarks", "created_at"),
    ("daily_questions", "created_at"),
    ("daily_attempts", "created_at"),
]

async def migrate_timestamp_columns(conn: AsyncConnection) -> int:
    """
    Inspects PostgreSQL information_schema and converts any existing
    TIMESTAMP WITHOUT TIME ZONE columns to TIMESTAMP WITH TIME ZONE.
    
    Returns the count of columns migrated.
    """
    if conn.dialect.name != "postgresql":
        logger.info(f"[Migration] Skipping PostgreSQL timezone migration for dialect: {conn.dialect.name}")
        return 0

    logger.info("[Migration] Checking PostgreSQL columns for TIMESTAMP WITH TIME ZONE compatibility...")

    # Query information_schema for columns that currently lack time zone
    check_query = text("""
        SELECT table_name, column_name 
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
          AND data_type = 'timestamp without time zone';
    """)

    result = await conn.execute(check_query)
    unmigrated = {(row[0], row[1]) for row in result.fetchall()}

    migrated_count = 0
    for table_name, column_name in TIMESTAMP_COLUMNS:
        if (table_name, column_name) in unmigrated:
            logger.info(f"[Migration] Migrating {table_name}.{column_name} -> TIMESTAMP WITH TIME ZONE (interpreting naive as UTC)...")
            alter_query = text(f"""
                ALTER TABLE public.{table_name} 
                ALTER COLUMN {column_name} TYPE TIMESTAMP WITH TIME ZONE 
                USING {column_name} AT TIME ZONE 'UTC';
            """)
            await conn.execute(alter_query)
            migrated_count += 1

    if migrated_count > 0:
        logger.info(f"[Migration] Successfully migrated {migrated_count} column(s) to TIMESTAMP WITH TIME ZONE.")
    else:
        logger.info("[Migration] All timestamp columns are already TIMESTAMP WITH TIME ZONE. Schema is up to date.")

    return migrated_count

async def run_cli_migration() -> None:
    """CLI entry point for running schema migration independently."""
    from app.core.database import engine
    logger.info("[Migration CLI] Starting database schema migration...")
    async with engine.begin() as conn:
        count = await migrate_timestamp_columns(conn)
    await engine.dispose()
    logger.info(f"[Migration CLI] Migration completed successfully. ({count} columns migrated)")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_cli_migration())
