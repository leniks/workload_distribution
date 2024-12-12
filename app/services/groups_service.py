from app.database import execute_query
from app.database import get_connection

class GroupsService:

    @classmethod
    def get_groups(cls):
        query = "SELECT * FROM groups;"
        return execute_query(query)

    @classmethod
    def insert_group(cls, number, student_count):
        query = "INSERT INTO groups (number, student_count) VALUES (%s, %s);"
        params = (number, student_count)
        execute_query(query, params)

