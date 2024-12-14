import streamlit as st
import pandas as pd
from app.services.loads_service import LoadsService
from app.services.teachers_service import TeacherService


def get_loads():
    loads = LoadsService.get_loads()
    if loads:
        df = pd.DataFrame(loads)
        st.dataframe(df)
    else:
        st.write("Нагрузки не найдены.")

def loads_handler():

    st.title("Управление нагрузками")

    button_container = st.container()

    with button_container:
        if st.button(label='Получить список нагрузок'):
            get_loads()

        if st.button(label='Добавить нагрузку'):
            st.session_state.show_form_add_load = True

        if st.button(label='Назначить преподавателя'):
            st.session_state.show_form_connect_load = True

        if st.button(label='Удалить нагрузку'):
            st.session_state.show_form_delete_load = True

    if 'show_form_add_load' not in st.session_state:
        st.session_state.show_form_add_load = False

    if 'show_form_connect_load' not in st.session_state:
        st.session_state.show_form_connect_load = False

    if 'show_form_delete_load' not in st.session_state:
        st.session_state.show_form_delete_load = False

    if st.session_state.show_form_add_load:
        if st.button(label='Скрыть форму добавления нагрузки'):
            st.session_state.show_form_add_load = False
            st.rerun()

        with st.form(key='create_load_form'):
            load_type = st.selectbox("Выберите тип нагрузки:", LoadsService.get_loads_enum())
            hours = st.number_input("Введите количество часов:", min_value=1, step=1)
            subjects = LoadsService.get_subjects()
            subject = st.selectbox("Выберите предмет:", subjects)
            groups = st.multiselect("Выберите группы:", LoadsService.get_groups())

            submit_add_button = st.form_submit_button(label='Подтвердить добавление')

            if submit_add_button:
                if not subject or not load_type or hours <= 0:
                    st.error("Пожалуйста, заполните все поля корректно.")
                else:
                    try:
                        result = LoadsService.insert_load(load_type, hours, subject, groups)
                        st.success(result)
                    except Exception as e:
                        st.error(f"Произошла ошибка: {str(e)}")

    if st.session_state.show_form_connect_load:
        if st.button(label='Скрыть форму назначения нагрузки'):
            st.session_state.show_form_connect_load = False
            st.rerun()

        with st.form(key='connect_load_form'):
            try:
                load = st.selectbox("Выберите нагрузку:", LoadsService.get_loads_and_hours())
                load_type = load.split(',')[0]
                subject = load.split(',')[2]
                status = load.split(',')[3]

                teacher = st.selectbox("Выберите преподавателя:", TeacherService.get_teachers_names())
            except AttributeError:
                st.text("Добавьте хотя бы одну нагрузку")


            submit_add_button = st.form_submit_button(label='Подтвердить назначение')

            if submit_add_button:
                if not load or not teacher:
                    st.error("Пожалуйста, заполните все поля корректно.")
                else:
                    result = LoadsService.connect_load_and_teacher(load_type, subject, teacher, status)
                    st.success(result)

    if st.session_state.show_form_delete_load:
        if st.button(label='Скрыть форму удаления нагрузки'):
            st.session_state.show_form_delete_load = False
            st.rerun()

        with st.form(key='delete_load_form'):
            try:
                load = st.selectbox("Выберите нагрузку:", LoadsService.get_loads_and_hours())
                load_type = load.split(',')[0]
                subject = load.split(',')[2]

            except AttributeError:
                st.text("Добавьте хотя бы одну нагрузку")

            submit_delete_button = st.form_submit_button(label='Подтвердить удаление')

            if submit_delete_button:
                if not load:
                    st.error("Пожалуйста, заполните все поля корректно.")
                else:
                    result = LoadsService.delete_load(load_type, subject)
                    st.success(result)