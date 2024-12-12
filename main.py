from app.pages.groups_page import groups_handler
from app.pages.competence_page import competencies_handler
import streamlit as st


# Главная логика приложения с навигацией
def main():
    st.sidebar.title("Навигация")
    page = st.sidebar.radio(
        "Перейти к странице",
        ["Управление группами", "Управление компетенциями" ],
    )
    if page == "Управление группами":
        groups_handler()

    elif page == "Управление компетенциями":
        competencies_handler()

if __name__ == "__main__":
    main()