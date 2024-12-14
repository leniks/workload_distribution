from app.pages.groups_page import groups_handler
from app.pages.competence_page import competencies_handler
from app.pages.subjects_page import subjects_handler
from app.pages.teachers_page import teachers_handler
from app.pages.loads_page import loads_handler
import streamlit as st


# Главная логика приложения с навигацией
def main():
    st.sidebar.title("Навигация")
    page = st.sidebar.radio(
        "Перейти к странице",
        ["Управление группами",
         "Управление компетенциями",
         "Управление предметами",
         "Управление преподавателями",
         "Управление нагрузками"],
    )
    if page == "Управление группами":
        groups_handler()

    elif page == "Управление компетенциями":
        competencies_handler()

    elif page == "Управление предметами":
        subjects_handler()

    elif page == "Управление преподавателями":
        teachers_handler()

    elif page == "Управление нагрузками":
        loads_handler()

if __name__ == "__main__":
    main()