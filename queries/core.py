from sqlalchemy import text, insert, select, update
from database import sync_engine, async_engine
from models import metadata_obj, workers_table
import asyncio
from models import Base

# ----------------------------------------------------------------------------

# text - функция преобразовывает текст запроса в вид, который понимает sqlalchemy при использовании сырых запросов
# insert - функция преобразовывает готовую таблицу для дальнейшей вставки информации в нее
# Base - базовый класс модели
# select - функция преобразовывает готовую таблицу для дальнейшего получения данных с нее

# ----------------------------------------------------------------------------

# создание таблиц в базе данных
def create_tables():
    sync_engine.echo = False # выключить логи
    # metadata_obj.drop_all() # удалить все таблицы
    # metadata_obj.create_all() # создать все таблицы
    Base.metadata.drop_all() # удалить все таблицы
    Base.metadata.create_all() # создать все таблицы
    sync_engine.echo = True # включить логи

class QueryCoreV1:
    """Класс представляет интерфейс по взаимодействию с бд с помощью сырых запросов"""

    # создание синхронной сессии с rollback для выполнения запросов к б.д.
    @staticmethod
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
    @staticmethod
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

    @staticmethod
    def insert_data():
        """Вставка значения в бд"""
        with sync_engine.connect() as conn:
            # выполнение запроса к б.д.
            conn.execute(
                text("INSERT INTO workers (username) VALUES ('Bobr'), ('Volk');") # сырой запрос можно писать только в text
            )

            # выполнить сохранение в бд
            conn.commit()

    @staticmethod
    def update_data(worker_id: int = 2, name: str = "Misha"):
        """Обновление значения в бд"""
        with sync_engine.connect() as conn:
            stmt = text('UPDATE workers SET username=:username WHERE id=:id')
            stmt = stmt.bindparams(username=name, id=worker_id)
            conn.execute(stmt)
            conn.commit()

class QueryCoreV2:
    """Класс представляет интерфейс по взаимодействию с бд в стиле query builder"""
    @staticmethod
    def insert_data_query_builder():
        # создание синхронной сессии с rollback для выполнения запросов к б.д. (в стиле query builder)
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

    @staticmethod
    def select_workers():
        """Получить записи с бд"""
        with sync_engine.connect() as conn:
            query = select(workers_table) # SELECT * FROM workers - подготовка запроса
            result = conn.execute(query) # выполнение запроса
            workers = result.one() # получение только одной записи (если больше, то ошибка)
            # workers = result.all() # получение всех записей
            # workers = result.one_or_none() # получение 0-1 запись (если больше, то ошибка)
            # workers = result.scalars().all() # получение всех записей только первого столбца
            print(workers)

    @staticmethod
    def update_workers(worker_id: int = 2, name: str = "Misha"):
        """Обновление значения бд"""
        with (sync_engine.connect() as conn):
            query = (
                update(workers_table)
                .values(username=name)
                # .where(workers_table.c.id==worker_id) # 1 способ указать какой элемент обновляем
                # .filter(workers_table.c.id==worker_id) # 2 способ указать какой элемент обновляем
                .filter_by(id=worker_id) # 3 способ указать какой элемент обновляем
            )
            conn.execute(query)
            conn.commit()