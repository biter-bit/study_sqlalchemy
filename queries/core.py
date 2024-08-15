from sqlalchemy import text, insert
from database import sync_engine, async_engine
from models import metadata_obj, workers_table
import asyncio

# ----------------------------------------------------------------------------

# text - функция преобразовывает текст запроса в вид, который понимает sqlalchemy при использовании сырых запросов
# insert - функция преобразовывает готовую таблицу для дальнейшей вставки информации в нее

# ----------------------------------------------------------------------------

# создание таблиц в базе данных
def create_tables():
    sync_engine.echo = False # выключить логи
    metadata_obj.drop_all() # удалить все таблицы
    metadata_obj.create_all() # создать все таблицы
    sync_engine.echo = True # включить логи

# создание синхронной сессии с rollback для выполнения запросов к б.д.
def get_123_sync():
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

# создание асинхронной сессии с rollback для выполнения запросов к б.д.
async def get_123_async():
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

# создание синхронной сессии с rollback для выполнения запросов к б.д. (в стиле сырого запроса)
def insert_data():
    with sync_engine.connect() as conn:
        # выполнение запроса к б.д.
        conn.execute(
            text("INSERT INTO workers (username) VALUES ('Bobr'), ('Volk');") # сырой запрос можно писать только в text
        )

        # выполнить сохранение в бд
        conn.commit()

# создание синхронной сессии с rollback для выполнения запросов к б.д. (в стиле query builder)
def insert_data_query_builder():
    with sync_engine.connect() as conn:
        # выполнение запроса к б.д. в стиле query builder
        conn.execute(
            insert(workers_table).values(
                [
                    {"username": "Bobr"},
                    {"username": "Volk"}
                ]
            )
        )

        # выполнить сохранение в бд
        conn.commit()

# ----------------------------------------------------------------------

# запуск асинхронной функции
asyncio.run(get_123_async())