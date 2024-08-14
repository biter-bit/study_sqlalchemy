from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from config import settings
import asyncio

# обьект синхронного движка по работе с б.д.
sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg, # url базы, к которой мы хотим подключиться
    echo=True, # включить логи б.д.
    pool_size=5, # максимальное кол-во подключений к б.д.
    max_overflow=10, # + дополнительное кол-во подключений к б.д.
)

# обьект асинхронного движка по работе с б.д.
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg, # url базы, к которой мы хотим подключиться
    echo=True, # включить логи б.д.
    pool_size=5, # максимальное кол-во подключений к б.д.
    max_overflow=10, # + дополнительное кол-во подключений к б.д.
)