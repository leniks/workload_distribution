import psycopg2
from app.config import settings
from app.database import get_connection
import os


def execute_sql_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql = file.read()

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()


absolute_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(absolute_path)))
ddl_file_path = os.path.join(parent_dir, 'migration', 'ddl.sql')
execute_sql_file(ddl_file_path)