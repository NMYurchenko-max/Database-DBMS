import psycopg2


def create_db(cur):
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(20),
            lastname VARCHAR(30),
            email VARCHAR(254) UNIQUE
        )""")
        print("Таблица clients создана.")
    except Exception as e:
        print(f"Ошибка при создании таблицы clients: {e}")

    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            number VARCHAR(11),
            client_id INTEGER REFERENCES clients(id)
        )""")
        print("Таблица phones создана.")
    except Exception as e:
        print(f"Ошибка при создании таблицы phones: {e}")


# 1. Функция для добавления структуры базы данных
def add_db(cur):
    create_db(cur)
    print("Всё успешно добавлено")
    return


# 2. Функция для удаления структуры базы данных
def delete_db(cur):
    cur.execute("""
        DROP TABLE clients, phones CASCADE;
        """)
    print("Всё успешно удалено")
    return


# 3. Функция для удаления таблицы
def delete_table(cur, table_name):

    cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
    print(f"Таблица {table_name} успешно удалена.")
    return


# 4. Функция для проверки существования таблиц в базе данных
def check_db(cur):
    # Получаем список всех таблиц в схеме 'public'
    cur.execute("""
    SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'public';
    """)
    all_tables = [row[0] for row in cur.fetchall()]

    # Список таблиц, которые мы ожидаем найти
    expected_tables = ['clients', 'phones', 'clients_phones']

    # Проверяем, существуют ли все ожидаемые таблицы
    for table in expected_tables:
        if table not in all_tables:
            print(f"Таблица '{table}' не найдена.")
        else:
            print(f"Таблица '{table}' найдена.")

    return


# 5. Функция для проверки существования данных в таблице
def check_table_data(cur, table_name, query):
    # Попытка выполнить SQL-запрос к базе данных
    try:
        # Выполняем SQL-запрос, переданный в качестве параметра
        cur.execute(query)
        # Получаем все строки результата запроса
        data = cur.fetchall()
        # Проверяем, есть ли данные
        if len(data) > 0:
            # Если данные найдены, выводим сообщение
            print(f"В таблице '{table_name}' найдены следующие данные:")
            # Проходим по всем строкам данных и выводим их
            for row in data:
                print(row)
        else:
            # Если данных нет, выводим соответствующее сообщение
            print(f"В таблице '{table_name}' нет данных.")
    # Обработка исключений, возникающих при выполнении запроса
    except Exception as e:
        # Выводим сообщение об ошибке
        print(f"Ошибка при выполнении запроса к таблице '{table_name}': {e}")
    return


# 6. Функции вставки данных в таблицы
def insert_client(cur, firstname, lastname, email, client_id=None):
    """
    Вставляет нового клиента в таблицу clients.
    Если client_id указан, предполагается,
    что это обновление существующего клиента.
    :param cur: курсор для выполнения SQL-запросов
    :param firstname: имя клиента
    :param lastname: фамилия клиента
    :param email: email клиента
    :param client_id: идентификатор клиента (опциональный)
    """
    # Инициализация параметров запроса вне условных блоков
    params = (firstname, lastname, email)
    if client_id is None:
        query = """
        INSERT INTO clients (firstname, lastname, email) VALUES (%s, %s, %s)
        ON CONFLICT (email) DO NOTHING
        """
    else:
        query = """
        UPDATE clients SET firstname=%s, lastname=%s, email=%s WHERE id=%s
        """
        # Добавляем client_id в параметры запроса, если он предоставлен
        params += (client_id,)

    cur.execute(query, params)
    print("Клиент успешно добавлен или обновлен.")


def insert_phone_with_check(cur, phone_data):
    """
    Вставляет новый номер телефона в таблицу phones,
    предварительно проверяет наличие client_id в таблице clients.
    :param cur: курсор для выполнения SQL-запросов
    :param phone_data: словарь с данными о номере телефона,
    включая 'number' и 'client_id'
    """
    client_id = phone_data['client_id']
    # Проверяем, существует ли client_id в таблице clients
    check_query = "SELECT * FROM clients WHERE id = %s;"
    cur.execute(check_query, (client_id,))
    result = cur.fetchone()
    if result is None:
        print(
            f"Client with ID {client_id} not found. \
                Cannot insert phone number.")
        return False
    # Если клиент найден, продолжаем вставку номера телефона
    insert_query = "INSERT INTO phones (number, client_id) VALUES (%s, %s);"
    cur.execute(insert_query, (phone_data['number'], client_id))
    print("Phone number successfully added.")
    return True


# 7. Функции поиска данных
# 7.1. Функция поиска данных по заданным условиям
def search_table_data(cur, table_name, conditions):
    where_clause = " AND ".join([f"{key} = %s" for key in conditions.keys()])
    query = f"""
    SELECT * FROM {table_name} WHERE {where_clause};
    """
    try:
        cur.execute(query, tuple(conditions.values()))
        data = cur.fetchall()
        if len(data) > 0:
            print(f"Найдены следующие данные в таблице '{table_name}':")
            for row in data:
                print(row)
        else:
            print(f"В таблице '{table_name}'\
                 нет данных, удовлетворяющих условиям.")
    except Exception as e:
        print(f"Ошибка при выполнении запроса к таблице '{table_name}': {e}")
    return


# 7.2. Простой поиск по имени и фамилии
def find_client_by_name(cur, firstname, lastname):
    """
    Параметры:
    cur: курсор для выполнения SQL-запросов
    firstname: имя клиента
    lastname: фамилия клиента
    """
    try:
        # Используем скобки для группировки условий,
        # чтобы избежать неправильной интерпретации логического выражения
        cur.execute(
            "SELECT * FROM clients WHERE (firstname = %s AND lastname = %s)",
            (firstname, lastname))
        data = cur.fetchall()
        if len(data) > 0:
            print("Найдены следующие данные в таблице 'clients': ")
            for row in data:
                print(row)
        else:
            print("В таблице 'clients' нет данных, удовлетворяющих условиям.")
    except Exception as e:
        print(f"Ошибка при выполнении запроса к таблице 'clients': {e}")
    return


# 7.3. Поиск по совпадений, когда известны только части данных
def find_client(cur, firstname=None, lastname=None, email=None, number=None):
    """
    Определение функции find_client,
    которая принимает курсор базы данных cur
    и необязательные параметры firstname, lastname, email,
    number и возвращает результат поиска по параметру для поиска клиентов.
    """
    # Если имя не указано, устанавливаем его значение как '%',
    # что означает поиск по любому имени.
    if firstname is None:
        firstname = '%'
    else:
        # Если имя указано, добавляем символы '%' с обеих сторон,
        # чтобы искать по любому имени.
        firstname = '%' + firstname + '%'

    # Если фамилия не указана, устанавливаем ее значение как '%',
    # что означает поиск по любой фамилии.
    if lastname is None:
        lastname = '%'
    else:
        # Если фамилия указана, добавляем символы '%' с обеих сторон,
        # чтобы искать по любой фамилии.
        lastname = '%' + lastname + '%'

    # Если email не указан, устанавливаем его значение как '%',
    # что означает поиск по любому email.
    if email is None:
        email = '%'
    else:
        # Если email указан, добавляем символы '%' с обеих сторон,
        # чтобы искать по любому email.
        email = '%' + email + '%'

    # Если номер телефона не указан, выполняем запрос
    # без условия по номеру телефона.
    if number is None:
        cur.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phonenumbers p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.lastname LIKE %s
            AND c.email LIKE %s
            """, (firstname, lastname, email))
    else:
        # Если номер телефона указан, добавляем условие
        # по номеру телефона в запрос.
        cur.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phonenumbers p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.lastname LIKE %s
            AND c.email LIKE %s AND p.number like %s
            """, (firstname, lastname, email, number))

    # Возвращаем результаты запроса.
    return cur.fetchall()


# 8. Функция обновления данных
# 8.1. телефонов
def update_phone_number(cur, old_number, new_number):
    """
    Обновляет номер телефона на новый для данного номера.
    :param cur: курсор для выполнения SQL-запросов
    :param old_number: старый номер телефона
    :param new_number: новый номер телефона
    """
    try:
        cur.execute("UPDATE phones SET number = %s WHERE number = %s",
                    (new_number, old_number))
        print("Номер телефона успешно обновлен.")
    except Exception as e:
        print(f"Ошибка при обновлении номера телефона: {e}")
        return


# 8.2. email
def update_client_email(cur, old_email, new_email):
    """
    Обновляет email на новый для данного email.
    :param cur: курсор для выполнения SQL-запросов
    :param old_email: старый email
    :param new_email: новый email
    """
    try:
        cur.execute("UPDATE clients SET email = %s WHERE email = %s",
                    (new_email, old_email))
        print("Email успешно обновлен.")
    except Exception as e:
        print(f"Ошибка при обновлении email: {e}")
        return


# 8.3. имени
def update_client_firstname(cur, old_firstname, new_firstname):
    """
    Обновляет имя на новое для данного имени.
    :param cur: курсор для выполнения SQL-запросов
    :param old_name: старое имя
    :param new_name: новое имя
    """
    try:
        cur.execute("UPDATE clients SET firstname = %s WHERE firstname = %s",
                    (new_firstname, old_firstname))
        print("Имя успешно обновлено.")
    except Exception as e:
        print(f"Ошибка при обновлении имени: {e}")
        return


# 8.4. фамилии
def update_client_lastname(cur, old_lastname, new_lastname):
    """
    Обновляет фамилию на новую для данной фамилии.
    :param cur: курсор для выполнения SQL-запросов
    :param old_lastname: старая фамилия
    :param new_lastname: новая фамилия
    """
    try:
        cur.execute("UPDATE clients SET lastname = %s WHERE lastname = %s",
                    (new_lastname, old_lastname))
        print("Фамилия успешно обновлена.")
    except Exception as e:
        print(f"Ошибка при обновлении фамилии: {e}")
        return


# 9. Функция добавления данных
# 9.1. клиентов
def add_client(cur, firstname, lastname, email):
    """
    Добавляет нового клиента в таблицу clients.
    :param cur: курсор для выполнения SQL-запросов
    :param firstname: имя клиента
    :param lastname: фамилия клиента
    :param email: email клиента
    """
    try:
        cur.execute(
            "INSERT INTO clients (firstname, lastname, email)"
            " VALUES (%s, %s, %s)",
            (firstname, lastname, email))
        print("Клиент успешно добавлен.")
    except Exception as e:
        print(f"Ошибка при добавлении клиента: {e}")


# 9.2. телефонов
def add_phone_number(cur, number, client_id):
    """
    Добавляет новый номер телефона для клиента в таблицу phones.
    :param cur: курсор для выполнения SQL-запросов
    :param number: номер телефона
    :param client_id: ID клиента, которому принадлежит номер
    """
    try:
        cur.execute("INSERT INTO phones (number, client_id) VALUES (%s, %s)",
                    (number, client_id))
        print("Номер телефона успешно добавлен.")
    except Exception as e:
        print(f"Ошибка при добавлении номера телефона: {e}")


# 9.3. почты
def add_client_email(cur, email, new_email):
    """
    Добавляет новый email для данного email.
    :param cur: курсор для выполнения SQL-запросов
    :param email: старый email
    :param new_email: новый email
    """
    try:
        cur.execute("UPDATE clients SET email = %s WHERE email = %s",
                    (new_email, email))
        print("Email успешно обновлен.")
    except Exception as e:
        print(f"Ошибка при обновлении email: {e}")
        return


# 10. Частичное удаление данных
# 10.1. Удаление клиента
def delete_client(cur, client_id):
    """
    Удаляет клиента из таблицы clients.
    :param cur: курсор для выполнения SQL-запросов
    :param client_id: ID клиента
    """
    try:
        cur.execute("DELETE FROM clients WHERE id = %s", (client_id,))
        print("Клиент успешно удален.")
    except Exception as e:
        print(f"Ошибка при удалении клиента: {e}")
        return


# 10.2. Удаление телефона
def delete_phone(cur, phone_id):
    """
    Удаляет телефон из таблицы phones.
    :param cur: курсор для выполнения SQL-запросов
    :param phone_id: ID телефона
    """
    try:
        cur.execute("DELETE FROM phones WHERE id = %s", (phone_id,))
        print("Телефон успешно удален.")
    except Exception as e:
        print(f"Ошибка при удалении телефона: {e}")
        return


# 10.3. Удаление почты
def delete_client_email(cur, email):
    """
    Удаляет email из таблицы clients.
    :param cur: курсор для выполнения SQL-запросов
    :param email: email
    """
    try:
        cur.execute("UPDATE clients SET email = NULL WHERE email = %s",
                    (email,))
        print("Email успешно обновлен.")
    except Exception as e:
        print(f"Ошибка при обновлении email: {e}")
        return


# Главная функция, которая выполняет подключение к базе данных,
# создание и удаление таблиц, выполнения запросов
def main():
    # Подключение к базе данных
    with psycopg2.connect(database="netology_db",
                          user="postgres",
                          password="postgres",
                          host="localhost") as conn:
        # Создание курсора для выполнения SQL-запросов
        with conn.cursor() as cur:
            # Удаление таблиц из базы данных
            delete_db(cur)
            # Создание таблиц в базе данных
            create_db(cur)
            # Добавление данных в таблицы
            insert_client(cur, "Иван", "Иванов", "ivan@gmail.com")
            insert_client(cur, "Пётр", "Петров", "ppetr@mail.ru")
            insert_client(cur, "Григорий", "Григорьев", "grish@outlook.com")
            insert_client(cur, "Семён", "Семёнов", "9913312643y@yandex.ru")
            insert_client(cur, "Андрей", "Андреев", "AAndreev@outlook.com")
            # Добавление номеров телефонов
            phone_data_list = [
                {'number': '79993318644', 'client_id': 1},
                {'number': '79993318645', 'client_id': 1},
                {'number': '79993318646', 'client_id': 2},
                {'number': '79993318647', 'client_id': 2},
                {'number': '79993318648', 'client_id': 3},
                {'number': '79993318649', 'client_id': 3},
                {'number': '79993318640', 'client_id': 4},
                {'number': '79993318641', 'client_id': 4},
                {'number': '79993318642', 'client_id': 5},
                {'number': '79993318643', 'client_id': 5}
            ]
            for phone_data in phone_data_list:
                insert_phone_with_check(cur, phone_data)

            # Завершаем транзакцию
            conn.commit()

            # Поиск клиентов по email
            conditions_email = {'email': 'ivan@gmail.com'}
            search_table_data(cur, 'clients', conditions_email)

            # Поиск клиентов по имени и фамилии
            conditions_name = {'firstname': 'Пётр', 'lastname': 'Петров'}
            search_table_data(cur, 'clients', conditions_name)

            # Проверка данных
            check_table_data(cur, 'phones', """
            SELECT number FROM phones WHERE number LIKE '%643%'
            """)

            # обновление (замена) телефона
            update_phone_number(cur, '79993318644', '79999999999')

            # Поиск клиентов по имени
            conditions_name = {'firstname': 'Семён'}
            search_table_data(cur, 'clients', conditions_name)

            # Поиск клиентов по email
            conditions_name = {'email': 'ivan@gmail.com'}
            search_table_data(cur, 'clients', conditions_name)

            # Поиск телефотов клиента
            conditions_name = {'client_id': 1}
            search_table_data(cur, 'phones', conditions_name)

            # Подтверждение транзакции
            conn.commit()

    print("Тестирование выполнено.")


# Вызов функции main()
# Запуск основной функции, если скрипт запущен как основной
if __name__ == '__main__':
    main()
