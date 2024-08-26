from sqlalchemy import text, insert, select, cast, func, Integer, and_
from sqlalchemy.orm import aliased

from database import sync_engine, async_engine, sync_session_factory, async_session_factory
from models import metadata_obj, WorkersOrm, ResumesOrm

# ---------------------------------------------------

# cast - приводит к указанному типу
# func - обьект, в котором хранятся функции sql
# func.avg(<столбец>) - взять среднее значение
# Integer - тип данных sql (int)
# and_() - функция оператора "и"
# aliased - функция по созданию псевдонима для класса

# ----------------------------------------------------

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
    def select_data_new(like_language: str = 'rus'):
        """Получение отфильрованных записей в бд

        SELECT workload, avg(compensation)::int as avg_compensation
        FROM resumes
        WHERE title like '%Python%' and compensation > 40000
        group by workload
        """
        with sync_session_factory() as sync_engine:
            query = (
                select(
                    ResumesOrm.workload, # получаем все записи из колонки title
                    cast(func.avg(ResumesOrm.compensation), Integer).label('avg_compensation'), # получаем средние значения из колонки title, приводим к int и называем "avg_title"
                )
                .select_from(ResumesOrm) # указываем с какой таблицы берем данные
                .filter(and_(
                    ResumesOrm.title.contains(like_language), # фильтруем по полю title, чтобы like_language был в title
                    ResumesOrm.compensation > 40000, # фильтруем по полю compensation > 40000
                ))
                .group_by(ResumesOrm.workload) # упорядочиваем по workload
                .having(cast(func.avg(ResumesOrm.compensation), Integer) > 70000) # позволяет доп. отфильтровать готовый результат
            )
            print(query.compile(compile_kwargs={"literal_binds": True})) # вывести запросы в бд при включенном echo с парамметрами
            res = sync_engine.execute(query) # выполни запрос
            result = res.all() # покажи все записи
            print(result)

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

    @staticmethod
    def join_cte_subquery_window_func(like_language: str = "Python"):
        """
        WITH helper2 AS (
            SELECT *, compensation-avg_workload_compensation AS compensation_diff
            FROM
            (SELECT
                w.id,
                w.username,
                r.compensation,
                r.workload,
                avg(r.compensation) OVER (PARTITION BY workload)::int AS avg_workload_compensation
            FROM resumes r
            JOIN workers = ON r.worker_id = w.id) helper1
        )
        SELECT * FROM helper2
        ORDER BY compensation_diff DESC;
        """
        with sync_session_factory() as session:
            r = aliased(ResumesOrm) # создание псевдонима
            w = aliased(WorkersOrm) # создание псевдонима
            # создаем подзапрос, получаем все записи таблицы resumes, workers и среднее значение по workload для каждой записи и приводим их к int
            subq = (
                select(
                    r,
                    w,
                    w.id.label("worker_id"),
                    func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label("avg_workload_compensation")
                )
                .join(r , r.worker_id == w.id) # чтобы сделать JOIN
                # .join(full=True) # чтобы сделать FULL JOIN
                # .join(isouter=True) # чтобы сделать LEFT JOIN
                .subquery('helper1') # называем наш подзапрос, т.е. алиас
            )
            # создаем общий запрос, получаем все записи подзапроса + разницу поля compensation и avg_workload_compensation
            cte = (
                select(
                    subq.c.worker_id,
                    subq.c.username,
                    subq.c.compensation,
                    subq.c.workload,
                    subq.c.avg_workload_compensation,
                    (subq.c.compensation - subq.c.avg_workload_compensation).label("compensation_diff"),
                )
                .cte("helper2")
            )
            # сортируем записи
            query = (
                select(cte)
                .order_by(cte.c.compensation_diff.desc())
            )

            res = session.execute(query)
            result = res.all()
            print(f'{result=}')