from src.dispatch.Logging import logging
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool

from alembic import context
import asyncio
from src.dispatch.db.session import SQLALCHEMY_DATABASE_URL

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url', SQLALCHEMY_DATABASE_URL)

log = logging.getLogger(__name__)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
from src.dispatch.db.session import Base
from src.dispatch.models import Quiz, Question, Choice, UserAttempt, UserAnswer
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

connectable = create_async_engine(SQLALCHEMY_DATABASE_URL, poolclass=pool.NullPool)

# 마이그레이션 실행 함수 (비동기 지원)
async def run_migrations():
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=Base.metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    log.info("Can't run migrations on offline mode")
else:
    # ✅ 비동기 마이그레이션 실행
    asyncio.run(run_migrations())
