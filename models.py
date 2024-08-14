from sqlalchemy import Table, Column, Integer, String, MetaData

# обьект метаданных, которые хранят данные таблиц, чтобы мы могли в дальнейшем с ними работать
metadata_obj = MetaData()

# обьект таблицы для б.д. или императивный стиль создания модели
workers_table = Table(
    "workers", # название таблицы
    metadata_obj, # метаданные таблицы
    Column("id", Integer, primary_key=True), # колонка таблицы с настройками типа и параметров
    Column("username", String), # колонка таблицы с настройками типа и параметров
)