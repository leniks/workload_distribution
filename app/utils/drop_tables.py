import psycopg2

conn = psycopg2.connect(dbname='postgres', user='postgres', password='123456', host='localhost', port=5431,)
cursor = conn.cursor()
try:
    conn.autocommit = True
    cursor.close()
    conn.close()
    cursor.execute("DROP DATABASE IF EXISTS postgres;")
finally:
    cursor.close()
    conn.close()