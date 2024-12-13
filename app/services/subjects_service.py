import psycopg2

from app.database import execute_query
from app.database import get_connection

def execute_procedure_subject(name, semestr_number, competences):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("CALL add_subject(%s, %s, %s)", (name, semestr_number, competences))
            conn.commit()

class SubjectService:
    @classmethod
    def get_subjects(cls):
        query = "SELECT name FROM subjects;"
        return execute_query(query)

    @classmethod
    def insert_subject(cls, name: str, semestr_number: int, competences):
        try:
            execute_procedure_subject(str(name), semestr_number, str(competences))
            return  "Предмет успешно добавлен!"
        except psycopg2.Error as err:
            return f"Ошибка: {err}"

    @classmethod
    def delete_subject(cls, name):
        query1 = "SELECT * FROM subjects WHERE name = %s;"
        params = (name,)
        subject = execute_query(query1, params)

        if subject:
            subject_id = subject[0][0]

            query2 = "DELETE FROM subjects WHERE id = %s;"
            params = (subject_id,)
            execute_query(query2, params)

            return f"Предмет '{name}' успешно удален."
        else:
            return f"Предмет '{name}' не найден."