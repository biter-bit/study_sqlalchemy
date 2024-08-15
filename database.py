from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine
from config import settings
import asyncio

# -------------------------------------------------------------------------

# create_async_engine - функция по созданию асинхронного движка по работе с бд
# async_sessionmaker - функция по созданию асинхронной сессии по работе с бд в стиле orm
# AsyncSession - класс по созданию асинхронной сессии по работе с бд в стиле orm
# Session - класс по созданию синхронной сессии по работе с бд в стиле orm
# sessionmaker - функция по созданию синхронной сессии по работе с бд в стиле orm
# create_engine - функция по созданию синхронного движка по работе с бд

# --------------------------------------------------------------------------

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

# синхронная сессия для выполнения запросов в стиле orm
sync_session_factory = sessionmaker(sync_engine)

# aсинхронная сессия для выполнения запросов в стиле orm
async_session_factory = async_sessionmaker(async_engine)