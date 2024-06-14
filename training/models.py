from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
#  Каждый класс модели, наследующий от этого Base,
# становится частью метаданных и используется для создания таблиц в БД.


# Определение модели Client
class Client(Base):
    # Указываем имя таблицы в базе данных
    __tablename__ = 'clients'
    # Определение столбца id как первичного ключа
    id = Column(Integer, primary_key=True)
    # Определение столбцов для имени и фамилии клиента
    first_name = Column(String(50))
    last_name = Column(String(50))
    # Определение уникального столбца email
    email = Column(String(100), unique=True)
    # Определение отношения между моделью Client и Phone
    phones = relationship('Phone', back_populates='client')

    # Определение метода __str__ для формата печати
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# Определение модели Phone
class Phone(Base):
    # Указываем имя таблицы в базе данных
    __tablename__ = 'phones'
    # Определение столбца id как первичного ключа
    id = Column(Integer, primary_key=True)
    # Определение столбца для номера телефона
    number = Column(String(20))
    # Определение внешнего ключа, связывающего телефон с клиентом
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    # Определение отношения между моделью Phone и Client
    client = relationship('Client', back_populates='phones')

    def __str__(self):
        return f"Телефон: {self.number}, Клиент: {self.client_id}"


# Определение ассоциативной таблицы для связи между клиентами и телефонами
phone_association = Table(
    'phone_client', Base.metadata,
    # Определение столбцов для идентификатора клиента и телефона
    Column('client_id', Integer, ForeignKey('clients.id')),
    Column('phone_id', Integer, ForeignKey('phones.id'))
)


import psycopg2

# Параметры подключения к базе данных
conn_params = {
    "dbname": "netology_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost"
}

try:
    # Подключение к базе данных
    with psycopg2.connect(**conn_params) as conn:
        # Создание курсора для выполнения запросов
        with conn.cursor() as cur:
            # Пример создания таблицы
            cur.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    email VARCHAR(100) UNIQUE
                );""")
            
            # Пример вставки данных
            cur.execute("""
                INSERT INTO clients (first_name, last_name, email) VALUES ('Иван', 'Иванов', 'ivanov@example.com');""")
            
            # Коммит изменений, чтобы сохранить их в базе данных
            conn.commit()
            
            # Пример выборки данных
            cur.execute("SELECT * FROM clients;")
            rows = cur.fetchall()
            for row in rows:
                print(row)
            
            # Закрытие соединения
finally:
    print("Соединение закрыто.")
except Exception as e:
    print(f"Ошибка: {e}")