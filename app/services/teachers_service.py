import psycopg2

from app.database import execute_query
from app.database import get_connection

def execute_procedure_teacher(name, available_workload, competences):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("CALL add_teacher(%s, %s, %s)", (name, available_workload, competences))
            conn.commit()

class TeacherService:
    @classmethod
    def get_teachers(cls):
        query = "SELECT * FROM teachers;"
        return execute_query(query)

    @classmethod
    def insert_teacher(cls, name: str, available_workload: int, competences):
        try:
            execute_procedure_teacher(str(name), available_workload, str(competences))
            return  "Преподаватель успешно добавлен!"
        except psycopg2.Error as err:
            return f"Ошибка: {err}"

    @classmethod
    def delete_teacher(cls, name):
        query1 = "SELECT * FROM teachers WHERE name = %s;"
        params = (name,)
        teacher = execute_query(query1, params)

        if teacher:
            teacher_id = teacher[0][0]

            query2 = "DELETE FROM teachers WHERE id = %s;"
            params = (teacher_id,)
            execute_query(query2, params)

            return f"Преподаватель '{name}' успешно удален."
        else:
            return f"Преподаватель '{name}' не найден."