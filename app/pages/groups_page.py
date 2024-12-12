import streamlit as st
import pandas as pd
from app.services.groups_service import GroupsService

def get_groups():
    groups = GroupsService.get_groups()
    if groups:
        df = pd.DataFrame(groups)
        st.dataframe(df)
    else:
        st.write("Группы не найдены.")


def groups_handler():
    st.title("Управление группами")

    button_container = st.container()  # Создаем контейнер для кнопок

    with button_container:
        if st.button(label='Получить список групп'):
            get_groups()

        if st.button(label='Добавить группу'):
            st.session_state.show_form_add_group = True

        if st.button(label='Удалить группу'):
            st.session_state.show_form_delete_group = True


    if 'show_form_add_group' not in st.session_state:
        st.session_state.show_form_add_group = False

    if 'show_form_delete_group' not in st.session_state:
        st.session_state.show_form_delete_group = False

    if st.session_state.show_form_add_group:
        if st.button(label='Скрыть форму добавления групп'):
            st.session_state.show_form_add_group = False
            st.rerun()

        with st.form(key='create_group_form'):

            group_add_number = st.text_input("Введите номер группы, которую нужно добавить:")
            student_add_count = st.text_input("Введите количество студентов в группе:")

            submit_add_button = st.form_submit_button(label='Подтвердить добавление')

            if submit_add_button:
                if not group_add_number or not student_add_count:
                    st.error("Пожалуйста, заполните оба поля: номер группы и количество студентов.")

                else:
                    try:
                        result = GroupsService.insert_group(group_add_number, int(student_add_count))
                        st.success(result)

                    except Exception as e:
                        st.error(f"Произошла ошибка: {str(e)}")

    if st.session_state.show_form_delete_group:
        if st.button(label='Скрыть форму удаления групп'):
            st.session_state.show_form_delete_group = False
            st.rerun()

        with st.form(key='delete_group_form'):

            group_delete_number = st.text_input("Введите номер группы, которую нужно удалить:")
            submit_delete_button = st.form_submit_button(label='Подтвердить удаление')

            if submit_delete_button:
                if not group_delete_number:
                    st.error("Пожалуйста, заполните номер группы.")

                else:
                    try:
                        result = GroupsService.delete_group(group_delete_number,)
                        st.success(result)

                    except Exception as e:
                        st.error(f"Произошла ошибка: {str(e)}")

