import psycopg2
from psycopg2 import sql
from app.config import settings

def get_connection():
    return psycopg2.connect(
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT
    )

def execute_query(query, params=None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
            conn.commit()

def execute_procedure(proc_name, params):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.callproc(proc_name, params)
            conn.commit()


def execute_many(query, params_list):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.executemany(query, params_list)
                conn.commit()
            except Exception as e:
                print(f"Ошибка: {e}")
