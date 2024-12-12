from app.database import execute_query

class CompetenceService:

    @classmethod
    def get_competencies(cls):
        query = "SELECT name FROM competencies;"
        return execute_query(query)

    @classmethod
    def insert_competence(cls, name):
        query1 = "SELECT * FROM competencies WHERE name = %s;"
        params = (name,)
        competence = execute_query(query1, params)

        if competence:
            return f"Компетенция '{name}' уже существует."
        else:
            query2 = "INSERT INTO competencies (name) VALUES (%s);"
            params = (name,)
            execute_query(query2, params)
            return f"Компетенция '{name}' успешно добавлена."

    @classmethod
    def delete_competence(cls, name):
        query1 = "SELECT * FROM competencies WHERE name = %s;"
        params = (name,)
        competence = execute_query(query1, params)

        if competence:
            competence_id = competence[0][0]

            query2 = "DELETE FROM competencies WHERE id = %s;"
            params = (competence_id,)
            execute_query(query2, params)

            return f"Компетенция '{name}' успешно удалена."
        else:
            return f"Компетенция '{name}' не найдена."