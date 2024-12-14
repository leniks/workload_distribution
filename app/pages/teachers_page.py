import streamlit as st
import pandas as pd
from app.services.teachers_service import TeacherService
from app.services.competences_service import CompetenceService

def get_teachers():

    teachers = TeacherService.get_teachers()
    if teachers:
        df = pd.DataFrame(teachers)
        df.columns = ['Имя', 'Распределённая нагрузка', 'Максимальная нагрузка', 'Компетенции']
        st.dataframe(df, hide_index=True)
    else:
        st.write("Преподаватели не найдены.")

def get_competencies():

    competencies = CompetenceService.get_competencies()
    # print(competencies)
    return [competency[0] for competency in competencies]

def teachers_handler():

    st.title("Управление преподавателями")

    button_container = st.container()

    with button_container:
        if st.button(label='Получить список преподавателей'):
            get_teachers()

        if st.button(label='Добавить преподавателя'):
            st.session_state.show_form_add_teacher = True

        if st.button(label='Удалить преподавателя'):
            st.session_state.show_form_delete_teacher = True

    if 'show_form_add_teacher' not in st.session_state:
        st.session_state.show_form_add_teacher = False

    if 'show_form_delete_teacher' not in st.session_state:
        st.session_state.show_form_delete_teacher = False

    if st.session_state.show_form_add_teacher:
        if st.button(label='Скрыть форму добавления преподавателя'):
            st.session_state.show_form_add_teacher = False
            st.rerun()

        with st.form(key='create_teacher_form'):
            teacher_name = st.text_input("Введите имя преподавателя")
            max_workload = st.number_input("Введите допустимую рабочую нагрузку:", min_value=1, step=1)
            competencies = get_competencies()
            selected_competencies = st.multiselect("Выберите компетенции преподавателя:", competencies)

            submit_add_button = st.form_submit_button(label='Подтвердить добавление')

            if submit_add_button:
                if not teacher_name or not selected_competencies:
                    st.error("Пожалуйста, заполните имя преподавателя и выберите хотя бы одну компетенцию.")
                else:
                    try:
                        competences_string = ','.join(selected_competencies)
                        result = TeacherService.insert_teacher(teacher_name, max_workload, competences_string)
                        st.success(result)
                    except Exception as e:
                        st.error(f"Произошла ошибка: {str(e)}")


    if st.session_state.show_form_delete_teacher:
        if st.button(label='Скрыть форму удаления преподавателя'):
            st.session_state.show_form_delete_teacher = False
            st.rerun()

        with st.form(key='delete_teacher_form'):
            teacher_delete_name = st.text_input("Введите имя преподавателя, которого нужно удалить:")
            submit_delete_button = st.form_submit_button(label='Подтвердить удаление')

            if submit_delete_button:
                if not teacher_delete_name:
                    st.error("Пожалуйста, заполните имя.")
                else:
                    try:
                        result = TeacherService.delete_teacher(teacher_delete_name)
                        st.success(result)
                    except Exception as e:
                        st.error(f"Произошла ошибка: {str(e)}")
