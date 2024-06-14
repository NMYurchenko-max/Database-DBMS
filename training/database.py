from sqlalchemy import (
    create_engine, Column, Integer, String, Table, ForeignKey)
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


# Создание базового класса для декларативного стиля определения моделей
Base = declarative_base()


# Определение ассоциативной таблицы для связи "многие ко многим"
association_table = Table(
    'phone_client', Base.metadata,
    # Определение столбцов для идентификатора клиента и телефона
    Column('client_id', Integer, ForeignKey('clients.id')),
    Column('phone_id', Integer, ForeignKey('phones.id'))
)


# Определение модели Client
class Client(Base):
    __tablename__ = 'clients'  # Имя таблицы
    id = Column(Integer, primary_key=True)  # Первичный ключ
    first_name = Column(String(50))  # Имя
    last_name = Column(String(50))  # Фамилия
    email = Column(String(100), unique=True)  # Email, уникальный
    phones = relationship(
        "Phone", secondary=association_table, back_populates="clients")
    # Отношение с Phone через ассоциативную таблицу

    # Метод __str__ для вывода информации о клиенте
    def __str__(self):
        return (
            f"Клиент: {self.first_name} "
            f"{self.last_name}, Email: {self.email}"
        )


# Определение модели Phone
class Phone(Base):
    __tablename__ = 'phones'  # Имя таблицы
    id = Column(Integer, primary_key=True)  # Первичный ключ
    number = Column(String(20))  # Номер телефона
    clients = relationship(
        "Client", secondary=association_table, back_populates="phones")
    # Добавляем обратную связь

    def __str__(self):
        return f"Телефон: {self.number}"


# Функция для создания структуры БД
def create_database():
    engine = create_engine(
        'postgresql+psycopg2://postgres:postgres@localhost/netology_db')
    # Подключение к БД
    Base.metadata.create_all(engine)  # Создание всех таблиц
    print("База данных успешно создана.")


# Функция для получения всех клиентов
def get_all_clients():
    session = sessionmaker(bind=create_engine(
        'postgresql+psycopg2://postgres:postgres@localhost/netology_db'))()
    # Сессия
    result = session.query(Client).all()
    # Выборка всех клиентов
    session.close()  # Закрытие сессии
    return result


# Функция для получения всех телефонов клиента
def get_all_phones(client_id):
    session = sessionmaker(bind=create_engine(
        'postgresql+psycopg2://postgres:postgres@localhost/netology_db'))()
    # Сессия
    result = session.query(Phone).filter_by(client_id=client_id).all()
    # Выборка всех телефонов
    session.close()  # Закрытие сессии
    return result


# Функция для получения клиента по id
def get_client_by_id(client_id):
    session = sessionmaker(bind=create_engine(
        'postgresql+psycopg2://postgres:postgres@localhost/netology_db'))()
    # Сессия
    result = session.query(Client).filter_by(id=client_id).first()
    # Выборка клиента по id
    session.close()  # Закрытие сессии
    return result


# Функция для добавления клиента
def add_client(first_name, last_name, email):
    session = sessionmaker(bind=create_engine(
        'postgresql+psycopg2://postgres:postgres@localhost/netology_db'))()
    # Сессия
    new_client = Client(
        first_name=first_name, last_name=last_name, email=email)
    # Новый клиент
    session.add(new_client)  # Добавление в сессию
    session.commit()  # Сохранение изменений
    session.close()  # Закрытие сессии


# Функция для добавления телефона клиенту
def add_phone_to_client(client_id, phone_number):
    session = sessionmaker(bind=create_engine(
        'postgresql+psycopg2://postgres:postgres@localhost/netology_db'))()
    try:
        phone = Phone(number=phone_number)  # Создаем новый телефон
        session.add(phone)  # Добавляем телефон в сессию
        client = session.query(Client).filter_by(id=client_id).first()
        # Находим клиента
        if client:
            client.phones.append(phone)  # Добавляем телефон к клиенту
            session.commit()  # Сохраняем изменения
        else:
            print(f"Клиент с ID {client_id} не найден.")
    finally:
        session.close()
    # Закрываем сессию в блоке finally - гарантировать закрытие в случае ошибок


# Функция для обновления данных клиента
def update_client_data(client_id, first_name=None, last_name=None, email=None):
    session = sessionmaker(bind=create_engine(
        'postgresql+psycopg2://postgres:postgres@localhost/netology_db'))()
    client = session.query(Client).filter_by(id=client_id).first()
    # Поиск клиента
    if first_name:
        client.first_name = first_name  # Обновление имени
    if last_name:
        client.last_name = last_name  # Обновление фамилии
    if email:
        client.email = email  # Обновление email
    session.commit()  # Сохранение изменений
    session.close()  # Закрытие сессии


# Функция для обновления номера телефона клиента
def update_phone_number(client_id, phone_id, new_number):
    session = sessionmaker(bind=create_engine(
        'postgresql+psycopg2://postgres:postgres@localhost/netology_db'))()
    client = session.query(Client).filter_by(id=client_id).first()
    # Поиск клиента
    client.phones[phone_id].number = new_number  # Обновление телефона
    session.commit()  # Сохранение изменений
    session.close()  # Закрытие сессии


# Функция для удаления телефона у клиента
def delete_phone_from_client(client_id, phone_id):
    session = sessionmaker(bind=create_engine(
        'postgresql+psycopg2://postgres:postgres@localhost/netology_db'))()
    client = session.query(Client).filter_by(id=client_id).first()
    # Поиск клиента
    client.phones.remove(session.query(Phone).get(phone_id))
    # Удаление телефона
    session.commit()  # Сохранение изменений
    session.close()  # Закрытие сессии


# Функция для удаления клиента
def delete_client(client_id):
    session = sessionmaker(bind=create_engine(
        'postgresql+psycopg2://postgres:postgres@localhost/netology_db'))()
    client = session.query(Client).filter_by(id=client_id).first()
    # Поиск клиента
    session.delete(client)  # Удаление клиента
    session.commit()  # Сохранение изменений
    session.close()  # Закрытие сессии


# Функция для поиска клиента
def find_client_by_info(info_type, value):
    session = sessionmaker(bind=create_engine(
        'postgresql+psycopg2://postgres:postgres@localhost/netology_db'))()
    if info_type == 'name':
        result = session.query(Client).filter_by(first_name=value).all()
        # Поиск по имени
    elif info_type == 'surname':
        result = session.query(Client).filter_by(last_name=value).all()
        # Поиск по фамилии
    elif info_type == 'email':
        result = session.query(Client).filter_by(email=value).all()
        # Поиск по email
    elif info_type == 'phone':
        result = session.query(Phone).filter_by(number=value).all()
        # Поиск по телефону
    else:
        result = None
    session.close()
    return result


# Точка входа в программу
if __name__ == '__main__':
    create_database()  # Создание БД
    add_client("Иван", "Иванов", "ivanov@example.com")  # Добавление клиента
    add_phone_to_client(1, "+79123456789")  # Добавление телефона
    update_client_data(1, first_name="Игорь", email="igorov@example.com")
    # Обновление данных
    delete_phone_from_client(1, 1)  # Удаление телефона
    delete_client(1)  # Удаление клиента
    clients = find_client_by_info('name', 'Иван')  # Поиск по имени
    for client in clients:
        print(client)  # Используем метод __str__ для печати
    phones = find_client_by_info('phone', '+79123456789')  # Поиск по телефону
    for phone in phones:
        print(phone)  # Используем метод __str__ для печати
