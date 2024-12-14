import psycopg2

from app.database import execute_query
from app.database import get_connection
from app.database import execute_many
from app.services.subjects_service import SubjectService
from app.services.groups_service import GroupsService
from app.services.teachers_service import TeacherService

class LoadsService:

    @classmethod
    def get_loads_enum(cls):
        query = "SELECT unnest(enum_range(NULL::loads_enum)) AS load_name;"
        res = execute_query(query)
        return [row[0] for row in res]

    @classmethod
    def get_loads_and_hours(cls):
        query = "SELECT load_type, hours, subject_name, connected FROM load_details;"
        res = execute_query(query)
        return [f'{row[0]}, {str(row[1])}ч., {row[2]}, {row[3]}' for row in res]

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
                query5 = "SELECT id FROM groups WHERE number = %s;"
                params = (group,)
                group_id = execute_query(query5, params)[0][0]
                group_ids.append(group_id)

            print(group_ids)
            print(load_id)
            query6 = "INSERT INTO groups_loads (group_id, loads_id) VALUES (%s, %s);"
            params_list = [(group_id, load_id) for group_id in group_ids]
            execute_many(query6, params_list)

            return f"Нагрузка успешно добавлена."

    @classmethod
    def get_available_load(cls, teacher_id):
        query = "SELECT get_available_load(%s);"
        return execute_query(query, (teacher_id,))[0][0]

    @classmethod
    def connect_load_and_teacher(cls, load_type: str, subject: str, teacher: str, status: str):
        if status.strip() == 'распределена':
            return "Выберите нераспределенную нагрузку."

        set_of_subject_comp = set(SubjectService.get_subjects_comp(subject))
        set_of_teacher_comp = set(TeacherService.get_teachers_comp(teacher))

        if not set_of_subject_comp.issubset(set_of_teacher_comp):
            return "Компетенции преподавателя не соответствуют нужным компетенциям для ведения предмета."

        query_subject_id = "SELECT id FROM subjects WHERE name = %s;"
        subject_id = execute_query(query_subject_id, (subject.strip(),))

        query_required_load = "SELECT hours FROM loads WHERE load_type = %s AND subject_id = %s;"
        required_load_params = (load_type, subject_id[0][0])
        subject_required_load = execute_query(query_required_load, required_load_params)

        subject_required_load = subject_required_load[0][0]
        teachers_available_load = LoadsService.get_available_load(teacher)

        if subject_required_load > teachers_available_load:
            return "Количество доступных часов для преподавателя меньше, чем нужно для ведения предмета."

        query_update_teacher = """
            UPDATE teachers
            SET occupied_load = occupied_load + %s
            WHERE name = %s;
        """
        execute_query(query_update_teacher, (subject_required_load, teacher))

        query_teacher_id = "SELECT id FROM teachers WHERE name = %s;"
        teacher_id = execute_query(query_teacher_id, (teacher,))

        query_load_id = "SELECT id FROM loads WHERE load_type = %s AND subject_id = %s;"
        load_id = execute_query(query_load_id, (load_type, subject_id[0][0]))

        query_update_load = """
            UPDATE loads
            SET teacher_id = %s, connected = TRUE
            WHERE id = %s;
        """
        execute_query(query_update_load, (teacher_id[0][0], load_id[0][0]))

        return "Нагрузка успешно назначена преподавателю."

    @classmethod
    def delete_load(cls, load_type, subject):
        query_subject_id = "SELECT id FROM subjects WHERE name = %s;"
        subject_id = execute_query(query_subject_id, (subject.strip(),))[0][0]
        try:
            query = """
            DELETE FROM loads 
            WHERE load_type = %s AND subject_id = %s
            """
            params = (load_type, subject_id)
            execute_query(query, params)
            return "Нагрузка удалена, преподавательские часы освобождены"
        except psycopg2.Error as err:
            return f"Ошибка: {err}"
