import psycopg2

from app.database import execute_query
from app.database import get_connection
from app.database import execute_many
from subjects_service import SubjectService

class LoadsService:

    @classmethod
    def get_loads_enum(cls):
        query = "SELECT unnest(enum_range(NULL::loads_enum)) AS load_name;"
        res = execute_query(query)
        return [row[0] for row in res]

    @classmethod
    def get_subjects(cls):
        res = SubjectService.get_subjects()
        return [row[0] for row in res]

    @classmethod
    def get_loads(cls):
        query = "SELECT * FROM load_details;"
        return execute_query(query)

    @classmethod
    def insert_load(cls, load_type: str, hours: int, subject: str, groups: list):
        query1 = "SELECT id FROM subjects WHERE name = %s;"
        params = (subject,)
        subject_id = execute_query(query1, params)[0][0]

        query2 = "SELECT * FROM loads WHERE load_type = %s AND subject_id = %s;"
        params = (load_type, subject_id)
        load = execute_query(query2, params)

        if load:
            return f"Такая нагрузка уже существует."
        else:
            query3 = "INSERT INTO loads (load_type, hours, subject_id) VALUES (%s, %s, %s) RETURNING id;"
            params = (load_type, hours, subject_id)
            load_id = execute_query(query3, params)

            group_ids = []
            for group in groups:
                query5 = "SELECT id FROM groups WHERE name = %s;"
                params = (group,)
                group_id = execute_query(query5, params)[0][0]
                group_ids.append(group_id)

            query6 = "INSERT INTO groups_loads (group_id, loads_id) VALUES (%s, %s);"
            params_list = [(group_id, load_id) for group_id in group_ids]
            execute_many(query6, params_list)

            return f"Нагрузка успешно добавлена."