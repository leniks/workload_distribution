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

# Пример функции для выполнения запроса
def execute_query(query, params=None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
            conn.commit()