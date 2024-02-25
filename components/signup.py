import streamlit as st
from util.extract_error_message import extract_error_message


def is_empty(value):
    return value is None or value == ""


def signup_ui(db_service, auth_service):
    st.title("Signup")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Signup", type='primary'):
        if is_empty(name):
            st.warning("Please provide your name")
            return
        if is_empty(email):
            st.warning("Please provide your email")
            return
        if is_empty(password):
            st.warning("Please provide your password")
            return
        try:
            user = auth_service.sing_up(email, password)
            st.session_state.user = user
            db_service.save_user_name_email(name, email)
            st.success("User registered successfully!")
        except Exception as e:
            st.error(extract_error_message(str(e)))
