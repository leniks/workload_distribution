import streamlit as st
import pandas as pd
from app.services.subjects_service import SubjectService
from app.services.competences_service import CompetenceService

def get_subjects():

    subjects = SubjectService.get_subjects()
    if subjects:
        df = pd.DataFrame(subjects)
        st.dataframe(df)
    else:
        st.write("Предметы не найдены.")

def get_competencies():

    competencies = CompetenceService.get_competencies()
    # print(competencies)
    return [competency[0] for competency in competencies]

def subjects_handler():

    st.title("Управление предметами")

    button_container = st.container()

    with button_container:
        if st.button(label='Получить список предметов'):
            get_subjects()

        if st.button(label='Добавить предмет'):
            st.session_state.show_form_add_subject = True

        if st.button(label='Удалить предмет'):
            st.session_state.show_form_delete_subject = True

    if 'show_form_add_subject' not in st.session_state:
        st.session_state.show_form_add_subject = False

    if 'show_form_delete_subject' not in st.session_state:
        st.session_state.show_form_delete_subject = False

    if st.session_state.show_form_add_subject:
        if st.button(label='Скрыть форму добавления предмета'):
            st.session_state.show_form_add_subject = False
            st.rerun()

        with st.form(key='create_subject_form'):
            subject_name = st.text_input("Введите название предмета:")
            semester_number = st.number_input("Введите номер семестра:", min_value=1, step=1)
            competencies = get_competencies()
            selected_competencies = st.multiselect("Выберите компетенции:", competencies)

            submit_add_button = st.form_submit_button(label='Подтвердить добавление')

            if submit_add_button:
                if not subject_name or not selected_competencies:
                    st.error("Пожалуйста, заполните название предмета и выберите хотя бы одну компетенцию.")
                else:
                    try:
                        competences_string = ','.join(selected_competencies)
                        result = SubjectService.insert_subject(subject_name, semester_number, competences_string)
                        st.success(result)
                    except Exception as e:
                        st.error(f"Произошла ошибка: {str(e)}")


    if st.session_state.show_form_delete_subject:
        if st.button(label='Скрыть форму удаления предмета'):
            st.session_state.show_form_delete_subject = False
            st.rerun()

        with st.form(key='delete_subject_form'):
            subject_delete_name = st.text_input("Введите название предмета, который нужно удалить:")
            submit_delete_button = st.form_submit_button(label='Подтвердить удаление')

            if submit_delete_button:
                if not subject_delete_name:
                    st.error("Пожалуйста, заполните название предмета.")
                else:
                    try:
                        result = SubjectService.delete_subject(subject_delete_name)
                        st.success(result)
                    except Exception as e:
                        st.error(f"Произошла ошибка: {str(e)}")
