from sqlalchemy import text, insert
from database import sync_engine, async_engine, sync_session_factory, async_session_factory
from models import metadata_obj, WorkersOrm

# создание таблиц в базе данных
def create_tables():
    sync_engine.echo = False # выключить логи
    metadata_obj.drop_all() # удалить все таблицы
    metadata_obj.create_all() # создать все таблицы
    sync_engine.echo = True # включить логи

# создание синхронной сессии с rollback для выполнения запросов к б.д. (в стиле ORM)
def insert_data():
    # создаем обьект записи таблицы
    worker_bobr = WorkersOrm(username="Bobr")

    with sync_session_factory() as sync_session:
        # sync_session.add_all([worker_bobr, worker_bobr]) # добавить несколько записей в сессию
        sync_session.add(worker_bobr) # добавляем запись в сессию
        sync_session.commit() # сохранить записи