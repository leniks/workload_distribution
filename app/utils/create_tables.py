import psycopg2
from app.utils.execute_sql_file import execute_sql_file
import os

absolute_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(absolute_path)))
ddl_file_path = os.path.join(parent_dir, 'migration', 'ddl.sql')
execute_sql_file(ddl_file_path)