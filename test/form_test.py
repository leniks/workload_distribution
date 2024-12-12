import streamlit as st

def main():
    st.title("Тестовая форма")

    with st.form(key='test_form'):
        text_input = st.text_input("Введите текст:")
        submit_button = st.form_submit_button(label='Отправить')

        if submit_button:
            st.write(f"Вы ввели: {text_input}")

if __name__ == "__main__":
    main()