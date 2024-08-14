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

# создание синхронной сессии с rollback для выполнения запросов к б.д.
with sync_engine.connect() as conn:
    # выполнение запроса к б.д.
    res = conn.execute(
        text("SELECT VERSION()") # сырой запрос можно писать только в text
    )

    # работает с данными в оперативной памяти, выводит все строки
    print(f"{res.all()=}")

    # работает с данными в оперативной памяти, выводит первую строку
    print(f"{res.first()=}")

    # выполнить сохранение в бд
    conn.commit()

# создание синхронной сессии с commit для выполнения запросов к б.д.
# with sync_engine.begin() as conn:
#     # выполнение запроса к б.д.
#     res = conn.execute(
#         text("SELECT VERSION()")  # сырой запрос можно писать только в text
#     )
#
#     # работает с данными в оперативной памяти, выводит все строки
#     print(f"{res.all()=}")
#
#     # работает с данными в оперативной памяти, выводит первую строку
#     print(f"{res.first()=}")








# обьект асинхронного движка по работе с б.д.
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg, # url базы, к которой мы хотим подключиться
    echo=True, # включить логи б.д.
    pool_size=5, # максимальное кол-во подключений к б.д.
    max_overflow=10, # + дополнительное кол-во подключений к б.д.
)

# создание асинхронной сессии с rollback для выполнения запросов к б.д.
async def get_123():
    async with async_engine.connect() as conn:
        # выполнение запроса к б.д.
        res = conn.execute(
            text("SELECT VERSION()") # сырой запрос можно писать только в text
        )

        # работает с данными в оперативной памяти, выводит все строки
        print(f"{res.all()=}")

        # работает с данными в оперативной памяти, выводит первую строку
        print(f"{res.first()=}")

        # выполнить сохранение в бд
        conn.commit()

# запуск асинхронной функции
asyncio.run(get_123())