from app.database import execute_query

def get_groups():
    query = "SELECT * FROM groups;"
    return execute_query(query)

def insert_group(number, student_count):
    query = "INSERT INTO groups (number, student_count) VALUES (%s, %s);"
    params = (number, student_count)
    execute_query(query, params)

get_groups()