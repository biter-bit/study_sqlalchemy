from sqlalchemy import text, insert, select
from database import sync_engine, async_engine, sync_session_factory, async_session_factory
from models import metadata_obj, WorkersOrm

# создание таблиц в базе данных
def create_tables():
    sync_engine.echo = False # выключить логи
    metadata_obj.drop_all() # удалить все таблицы
    metadata_obj.create_all() # создать все таблицы
    sync_engine.echo = True # включить логи

class ORMQuery:
    # создание синхронной сессии с rollback для выполнения запросов к б.д. (в стиле ORM)
    @staticmethod
    def insert_data():
        with sync_session_factory() as sync_session:
            # создаем обьект записи таблицы
            worker_bobr = WorkersOrm(username="Bobr")
            # sync_session.add_all([worker_bobr, worker_bobr]) # добавить несколько записей в сессию
            sync_session.add(worker_bobr) # добавляем запись в сессию
            sync_session.flush() # отправляет запросы в бд, но не выполняет их (возвращает данные автоинкремента)
            sync_session.commit() # сохранить записи

    @staticmethod
    def select_data():
        """Получение всех записей из бд"""
        with sync_session_factory() as sync_session:
            worker_id = 1
            query = select(WorkersOrm)  # SELECT * FROM workers - подготовка запроса
            result = sync_session.execute(query)  # выполнение запроса
            # workers = result.one()  # получение только одной записи (если больше, то ошибка)
            workers = result.all() # получение всех записей
            # workers = result.one_or_none() # получение 0-1 запись (если больше, то ошибка)
            # workers = result.scalars().all() # получение всех записей только первого столбца
            print(workers)

    @staticmethod
    def select_data_one():
        """Получение одной записи из бд"""
        with sync_session_factory() as sync_session:
            worker_id = 1
            worker_jack = sync_session.get(WorkersOrm, worker_id) # первый способ получения элемента
            # worker_jack = sync_session.get(WorkersOrm, {"id": worker_id}) # второй способ получения элемента
            # worker_jack = sync_session.get(WorkersOrm, (worker_id, 'hello')) # третий способ получения элемента

    @staticmethod
    def update_data(worker_id: int = 2, name: str = "Misha"):
        """Изменение записи в бд"""
        with sync_session_factory() as sync_session:
            worker_jack = sync_session.get(WorkersOrm, worker_id)  # получения элемента
            worker_jack.username = name # изменение записи
            # sync_session.expire() # сброс 1 записи в сессии, запрос в базу не отправляет
            sync_session.expire_all() # сброс всех изменений в сессии, запрос в базу не отправляет
            # sync_session.refresh(worker_jack) # сброс конкретной записи до значений как в бд
            sync_session.commit() # сохранение записи