from app.database import execute_query

class GroupsService:

    @classmethod
    def get_groups(cls):
        query = "SELECT number, student_count FROM groups;"
        return execute_query(query)

    @classmethod
    def get_groups_names(cls):
        query = "SELECT number FROM groups;"
        return execute_query(query)

    @classmethod
    def insert_group(cls, number, student_count):
        query1 = "SELECT * FROM groups WHERE number = %s;"
        params = (number,)
        group = execute_query(query1, params)

        if group:
            return f"Группа с номером {number} уже существует."
        else:
            query2 = "INSERT INTO groups (number, student_count) VALUES (%s, %s);"
            params = (number, student_count)
            execute_query(query2, params)
            return f"Группа с номером {number} успешно добавлена."

    @classmethod
    def delete_group(cls, number):
        query1 = "SELECT * FROM groups WHERE number = %s;"
        params = (number,)
        group = execute_query(query1, params)

        if group:
            group_id = group[0][0]

            query3 = "DELETE FROM loads WHERE id IN (SELECT loads_id FROM groups_loads WHERE group_id = %s);"
            params = (group_id,)
            execute_query(query3, params)

            query2 = "DELETE FROM groups WHERE id = %s;"
            params = (group_id,)
            execute_query(query2, params)

            return f"Группа с номером {number} и принадлежащие ей нагрузки успешно удалены."
        else:
            return f"Группа с номером {number} не найдена."