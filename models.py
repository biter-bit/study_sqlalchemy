import datetime
from typing import Optional, Annotated

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from enum import Enum

# -----------------------------------------------------------------------------

# Table - класс представления таблицы
# Column - класс представления поля в таблице
# Integer - класс представляет тип поля integer
# String - класс представляет тип поля string
# MetaData - класс представляет собой метаданные для таблицы бд
# Mapped - класс представляет собой преобразователь типа в тип sql
# mapped_column - функция возвращает настройки для данного поля
# Optional - указывает на то, что переменная может быть None
# Enum - позволяет удобно работать с свойствами класса (получать имя переменной и значение свойства, итерироваться по ним)
# ForeignKey - внешний ключ
# func - это обьект, в котором функции sql
# Annotated - указывает на тип и значение, которое будет у переменной

# -------------------------------------------------------------------------------------

# --------------------------------Декларативный стиль---------------------------------------

intpk = Annotated[int, mapped_column(primary_key=True)]
str_256 = Annotated[str, 256]

class Base(DeclarativeBase):
    """Базовый класс для работы с ORM"""
    type_annotation_map = {
        str_256: String(256)
    } # создание кастомных форматов типа

    def __repr__(self):
        """Используется для красивого вывода результата запроса"""
        return 'Hello'

class WorkersOrm(Base):
    """Представляет модель таблицы базы данных"""
    # название таблицы
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]

    resumes: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="workers",
        primaryjoin="and_(WorkersOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == 'parttime')", # подгрузит только те записи, которые соблюдают условиям
        order_by="ResumesOrm.id.desc()", # сортирует записи
        lazy="selectin" # убрать ленивую подгрузку и добавить selectin
    )

class Workload(Enum):
    HELLO = 'hello'
    BYE = 'bye'

class ResumesOrm(Base):
    """Представляет модель таблицы базы данных"""
    # название таблицы
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True) # поле уникального идентификатора
    id_2: Mapped[intpk] # поле уникального идентификатора
    title: Mapped[str_256] # поле с форматом типа str_256
    compensation: Mapped[str] = mapped_column(nullable=True) # поле может быть null
    compensation2: Mapped[str | None]  # поле может быть null
    compensation3: Mapped[Optional[str]]  # поле может быть null
    workload: Mapped[Workload] # поле может быть только из указанных в классе Workload
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id")) # указывает на внешний ключ
    worker2_id: Mapped[int] = mapped_column(ForeignKey(WorkersOrm.id)) # указывает на внешний ключ
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())")) # указать дату создания по умолчанию во временной зоне utc на стороне бд
    created_at_2: Mapped[datetime.datetime] = mapped_column(server_default=func.now()) # указать дату создания по умолчанию во временной зоне utc на стороне бд
    created_at_3: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow()) # указать дату создания по умолчанию во временной зоне utc на стороне приложения
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow(),
        onupdate=datetime.datetime.utcnow
    ) # указать дату обновления по умолчанию во временной зоне utc на стороне приложения

    workers: Mapped["WorkersOrm"] = relationship(
        back_populates="resumes", # уберает предупреждения sqlalchemy + убирает поле resumes из обьекта workers
        # backref='resumes', # создает запись resumes для связанной таблицы (не нужно прописывать связь вручную)
    )

    # добавляем типы и формат полей
    __table_args__ = (

    )

# ----------------------------Императивный стиль------------------------------------------

# обьект метаданных, которые хранят данные таблиц, чтобы мы могли в дальнейшем с ними работать
metadata_obj = MetaData()

# обьект таблицы для б.д. или императивный стиль создания модели
workers_table = Table(
    "workers", # название таблицы
    metadata_obj, # метаданные таблицы
    Column("id", Integer, primary_key=True), # колонка таблицы с настройками типа и параметров
    Column("username", String), # колонка таблицы с настройками типа и параметров
)