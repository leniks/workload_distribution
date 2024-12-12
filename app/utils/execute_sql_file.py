from app.config import settings
from app.database import get_connection


def execute_sql_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql = file.read()

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()