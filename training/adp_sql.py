import psycopg2

params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "postgres",
    "port": "5432",
    "sslmode": "disable",
    "application_name": "adp_sql",
    "connect_timeout": "10"
}

try:
    conn = psycopg2.connect(**params)
    print("Opened database successfully")

    # Создаем курсор
    cur = conn.cursor()

    # Проверяем существование схемы и создаем ее, если необходимо
    cur.execute('CREATE SCHEMA IF NOT EXISTS adp;')

    # Устанавливаем search_path через SQL-запрос
    cur.execute('SET search_path TO adp;')

    # Создаем таблицу, указывая схему
    cur.execute('''CREATE TABLE adp.COMPANY
               (ID INT PRIMARY KEY     NOT NULL,
               NAME           TEXT    NOT NULL,
               AGE            INT     NOT NULL,
               ADDRESS        CHAR(50),
               SALARY         REAL);''')
    print("Table created successfully")

    # Завершаем транзакцию
    conn.commit()

    # Закрываем соединение
    conn.close()
    print("Database connection closed")
except Exception as e:
    print(f"An error occurred: {e}")
