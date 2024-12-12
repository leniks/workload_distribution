from app.pages.groups_page import groups_handler
import streamlit as st


# Главная логика приложения с навигацией
def main():
    st.sidebar.title("Навигация")
    page = st.sidebar.radio(
        "Перейти к странице",
        ["Управление группами",],
    )
    if page == "Управление группами":
        groups_handler()

if __name__ == "__main__":
    main()