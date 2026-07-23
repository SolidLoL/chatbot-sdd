import asyncio
from logging.config import fileConfig

from alembic import context
from asyncpg import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = None


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    from sqlalchemy import text

    connectable = create_async_engine(settings.DATABASE_URL)

    async with connectable.connect() as conn:
        await conn.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online():
    """Connect to the database directly via asyncpg URL and run migrations."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
