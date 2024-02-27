import streamlit as st
from util.extract_error_message import extract_error_message


def is_empty(value):
    return value is None or value == ""


def login_ui(auth_service):
    st.title("Login")
    email = st.text_input(label="Email")
    password = st.text_input(label="Password", type="password")

    if st.button("Login", type='primary'):
        if is_empty(email):
            st.warning("Please provide your email")
            return
        if is_empty(password):
            st.warning("Please provide your password")
            return
        try:
            user = auth_service.sign_in(email, password)
            st.session_state.user = user
            st.success(f"Welcome {user['email']}")
        except Exception as e:
            st.error(extract_error_message(str(e)))
