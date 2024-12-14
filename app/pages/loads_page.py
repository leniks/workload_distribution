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

    if 'show_form_add_load' not in st.session_state:
        st.session_state.show_form_add_load = False

    if 'show_form_connect_load' not in st.session_state:
        st.session_state.show_form_connect_load = False

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
            load = st.selectbox("Выберите нагрузку:", LoadsService.get_loads_and_hours())
            load_type = load.split(',')[0]
            subject = load.split(',')[-1]

            teacher = st.selectbox("Выберите преподавателя:", TeacherService.get_teachers_names())

            submit_add_button = st.form_submit_button(label='Подтвердить назначение')

            if submit_add_button:
                if not load or not teacher:
                    st.error("Пожалуйста, заполните все поля корректно.")
                else:
                    result = LoadsService.connect_load_and_teacher(load_type, subject, teacher)
                    st.success(result)
