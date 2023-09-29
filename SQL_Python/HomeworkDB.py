import psycopg2
import sys


# Создание таблиц базы данных
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""DROP TABLE IF EXISTS phones""")
        cur.execute("""DROP TABLE IF EXISTS clients""")
        cur.execute(
            """CREATE TABLE clients
                    (client_id SERIAL PRIMARY KEY, 
                    first_name VARCHAR(40) NOT NULL, 
                    last_name VARCHAR(40) NOT NULL, 
                    email VARCHAR(40) NOT NULL CHECK (email ~* '@'),
                    UNIQUE(first_name, last_name, email));"""
        )
        cur.execute(
            """CREATE TABLE phones
                    (phone_id SERIAL PRIMARY KEY, 
                    phone_number VARCHAR(11) NOT NULL CHECK (phone_number ~ '^\d+$'), 
                    client_id int NOT NULL REFERENCES clients(client_id),
                    UNIQUE(phone_number, client_id));"""
        )
        conn.commit()
    print("База данных успешно создана")


# Получение id клиента
def _get_client_id(
    conn, first_name=None, last_name=None, email=None, phone_number=None
):
    with conn.cursor() as cur:
        if first_name and last_name:
            cur.execute(
                """SELECT client_id
                             FROM clients
                            WHERE first_name = '{}' AND last_name = '{}';""".format(
                    first_name, last_name
                )
            )
        elif email:
            cur.execute(
                """SELECT client_id
                             FROM clients
                            WHERE email = '{}';""".format(
                    email
                )
            )
        elif phone_number:
            cur.execute(
                """SELECT client_id
                             FROM phones
                            WHERE phone_number = '{}';""".format(
                    phone_number
                )
            )
        else:
            print(
                "Недостаточно информации для поиска. Необходимо ввести имя и фамилию, либо email, либо номер телефона!"
            )
            sys.exit(1)
        client_id = cur.fetchone()
        if client_id:
            return client_id[0]
        else:
            print("Клиент не найден. Проверьте правильность введенной информации")
            sys.exit(1)


# Добавление нового уникального клиента
def add_new_client(conn, first_name, last_name, email, phone_number=None):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO clients(first_name, last_name, email) 
                        VALUES('{}', '{}', '{}') 
                        RETURNING client_id;""".format(
                    first_name, last_name, email
                )
            )
            client_id = cur.fetchone()[0]
            if phone_number:
                add_phone_number(conn, phone_number, client_id=client_id)
        print("Клиент успешно добавлен")
    except psycopg2.errors.UniqueViolation:
        print("Клиент уже существует в базе")
    except psycopg2.errors.CheckViolation:
        print("Проверьте правильность вводимых данных")


# Добавление номера к существующему клиенту
def add_phone_number(
    conn, phone_number, first_name=None, last_name=None, email=None, client_id=None
):
    try:
        if not client_id:
            client_id = _get_client_id(
                conn, first_name=first_name, last_name=last_name, email=email
            )
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO phones(phone_number, client_id) 
                        VALUES({}, {});""".format(
                    phone_number, client_id
                )
            )
            conn.commit()
    except psycopg2.errors.UniqueViolation:
        print("Номер телефона уже существует в базе данных")


# Удаление номера клиента
def delete_phone_number(
    conn, first_name=None, last_name=None, email=None, client_id=None
):
    if not client_id:
        client_id = _get_client_id(
            conn, first_name=first_name, last_name=last_name, email=email
        )
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM phones WHERE client_id = {};""".format(client_id))
        conn.commit()


# Удаление информации о клиенте
def delete_client(conn, first_name=None, last_name=None, email=None):
    client_id = _get_client_id(
        conn, first_name=first_name, last_name=last_name, email=email
    )
    with conn.cursor() as cur:
        delete_phone_number(conn, client_id=client_id)
        cur.execute("""DELETE FROM clients WHERE client_id = {};""".format(client_id))
        conn.commit()
    print("Клиент удален")


# Поиск и вывод id клиента
def find_client_id(
    conn, first_name=None, last_name=None, email=None, phone_number=None
):
    client_id = _get_client_id(conn, first_name, last_name, email, phone_number)
    print("Id клиента:", client_id)


# Изменение данных клиента
def change_client_info(
    conn,
    first_name=None,
    last_name=None,
    email=None,
    phone_number=None,
    new_first_name=None,
    new_last_name=None,
    new_email=None,
):
    client_id = _get_client_id(
        conn,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
    )
    with conn.cursor() as cur:
        if new_first_name:
            cur.execute(
                """UPDATE clients SET first_name = '{}' WHERE client_id = {};""".format(
                    new_first_name, client_id
                )
            )
        if new_last_name:
            cur.execute(
                """UPDATE clients SET last_name = '{}' WHERE client_id = {};""".format(
                    new_last_name, client_id
                )
            )
        if new_email:
            cur.execute(
                """UPDATE clients SET email = '{}' WHERE client_id = {};""".format(
                    new_email, client_id
                )
            )
        conn.commit()
    print("Данные успешно изменены")


with psycopg2.connect(
    database="netology_db",
    user="admin",
    password="admin",
    host="localhost",
    port="5432",
) as conn:
    create_db(conn)
    # add_new_client(conn,'Kola', 'Whote', 'Kol@mail.ru', '79961542260')
    # add_new_client(conn,'Nick', 'Mill', 'Nick@mail.ru', '76549823154')
    # add_phone_number(conn, '79961681460', email='Nick@mail.ru')
    # delete_client(conn, first_name = 'Nick', last_name = 'Mill')
    # delete_phone_number(conn, first_name = 'Kola', last_name = 'Whote')
    # find_client_id(conn, email='Nick@mail.ru')
    # change_client_info(conn, first_name = 'Kola', last_name = 'Whote', new_first_name='Berra', new_email='Berra@mail.ru')
