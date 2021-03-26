from peewee import *

# Создаем соединение с нашей базой данных
# В нашем примере у нас это просто файл базы
conn = SqliteDatabase('NoteNew.db')

# Определяем базовую модель о которой будут наследоваться остальные
class BaseModel(Model):
    class Meta:
        database = conn  # соединение с базой, из шаблона выше

# Определяем модель исполнителя
class Note(BaseModel):
    id = AutoField(column_name='NoteId')
    title = TextField(column_name='Title', null=True)
    text = TextField(column_name='Text', null=True)
    # tags = CharField(column_name='Tags', null=True) # CharField ?? смотреть на джоины
    
    class Meta:
        table_name = 'Note'

class Tag(BaseModel):
    id = AutoField(column_name='TagId')
    tag = TextField(column_name='Tag', null=True, unique=True) # один тег - одна модель, обработка тегов

    class Meta:
        table_name = 'Tag'

class TagNote(BaseModel):
    note = ForeignKeyField(Note, to_field='id', unique=True)
    tag = ForeignKeyField(Tag, to_field='id')

    class Meta:
        table_name = 'TagNote'

# Создаем курсор - специальный объект для запросов и получения данных с базы
cursor = conn.cursor()

# Закомментировать после первого запуска
conn.create_tables([Note], safe = True)
conn.create_tables([Tag], safe = True)
conn.create_tables([TagNote], safe = True)

# Не забываем закрыть соединение с базой данных
conn.close()
