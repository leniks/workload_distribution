import streamlit as st
import pandas as pd
from app.services.competences_service import CompetenceService

def get_competencies():
    competencies = CompetenceService.get_competencies()
    if competencies:
        df = pd.DataFrame(competencies)
        st.dataframe(df)
    else:
        st.write("Компетенции не найдены.")


def competencies_handler():
    st.title("Управление компетенциями")

    button_container = st.container()  # Создаем контейнер для кнопок

    with button_container:
        if st.button(label='Получить список компетенций'):
            get_competencies()

        if st.button(label='Добавить компетенцию'):
            st.session_state.show_form_add_competence = True

        if st.button(label='Удалить компетенцию'):
            st.session_state.show_form_delete_competence = True


    if 'show_form_add_competence' not in st.session_state:
        st.session_state.show_form_add_competence = False

    if 'show_form_delete_competence' not in st.session_state:
        st.session_state.show_form_delete_competence = False

    if st.session_state.show_form_add_competence:
        if st.button(label='Скрыть форму добавления компетенции'):
            st.session_state.show_form_add_competence = False
            st.rerun()

        with st.form(key='create_competence_form'):

            competence_add = st.text_input("Введите название компетенции, которую нужно добавить:")

            submit_add_button = st.form_submit_button(label='Подтвердить добавление')

            if submit_add_button:
                if not competence_add:
                    st.error("Введите компетенцию, которую нужно добавить.")

                else:
                    try:
                        result = CompetenceService.insert_competence(competence_add,)
                        st.success(result)

                    except Exception as e:
                        st.error(f"Произошла ошибка: {str(e)}")

    if st.session_state.show_form_delete_competence:
        if st.button(label='Скрыть форму удаления компетенций'):
            st.session_state.show_form_delete_competence = False
            st.rerun()

        with st.form(key='delete_competence_form'):

            competence_delete = st.text_input("Введите компетенцию, которую нужно удалить.")
            submit_delete_button = st.form_submit_button(label='Подтвердить удаление')

            if submit_delete_button:
                if not competence_delete:
                     st.error("Пожалуйста, заполните название компетенции.")

                else:
                    try:
                        result = CompetenceService.delete_competence(competence_delete,)
                        st.success(result)

                    except Exception as e:
                        st.error(f"Произошла ошибка: {str(e)}")

