import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Course, Homework

DNS = 'postgresql://postgres@localhost:5432/netology_db'
engine = sqlalchemy.create_engine(DNS)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()
# создаем экзмпляр course
course1 = Course(name='Python')
print(course1.id)  # Выдаст None

session.add(course1)    # необходимо добавить сессию и коммит
sessionmaker.commit()

print(course1.id)   # Выдаст 1

print(course1)  # в моделе прописали __str__, выдает теперь полную ин 1: Python

# создаем экзмпляр домашней работы
hw1 = Homework(number=1, description='простая домашняя работа', course=course1)
hw2 = Homework(numder=2, description='сложная домашняя работа', course=course1)
# добавляем эти объекты в сессию, чтобы отправить их в базу данных
# session.add(hw1)
session.add_all([hw1, hw2])
sessionmaker.commit()

# извлечение данных - метод query
for c in session.query(Course).all():
    # хотим достать все курсы
    print(c)
# аналогично для домашних работ
for c in session.query(Homework).all():
    print(c)


# извлечение данных - метод filter
for c in session.query(Course).filter(Course.name == 'Python').all():
    print(c)
for c in session.query(Homework).filter(Homework.number > 1).all():
    print(c)

# использование like
for c in session.query(Course).filter(Course.name.like('P%')).all():
    print(c)
for c in session.query(Homework.description.like('%слож%')).all():
    print(c)

# Объединение. Сначала указать исходную таблицу
# и применить метод join - указать 2-ю табл и свойство relationship
# для связи,определено в модели.
# Далее ставим all, или условия (например HW №=2)
for c in session.query(Course).join(
        Homework.course).filter(Homework.number == 2).all():
    print(c)

# Вложенные подзапросы subq, в конце добавляется subquery()
# Чтобы было более интересно, создадим сначала новый курс
course2 = Course(name='Java')
session.add(course2)
session.commit()

# сначала пишем подзапрос
subq = session.query(Homework).filter(
    Homework.description.like('%слож%')).subquery()
# основной запрос - достать курсы, в которых есть сложная дом. работа
# и объединить с подзапросом (subq) и условие объединения
# когда непонятно как объединить произвольную таблицу - условие задать явно
for c in session.query(Course).join(subq, Course.id == subq.c.course_id).all():
    print(c)
# subq.c - результат подзапроса (хранение в поле 'с' поумолчанию)

# Обновление объектов
# сначала найти, обновить и закоммитить
session.query(Course).filter(Course.name == 'Java').update(
    {'name': 'JavaScript'})
session.commit()

# удаление объектов delete, аналогично
session.query(Course).filter(Course.name == 'JavaScript').delete()
session.commit()

# выведем все курсы
for c in session.query(Course).all():
    print(c)
