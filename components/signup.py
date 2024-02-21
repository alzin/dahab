import streamlit as st
from util.extract_error_message import extract_error_message


def is_empty(value):
    return value is None or value == ""


def signup_ui(auth_service):
    st.title("Signup")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Signup"):
        if is_empty(email):
            st.warning("Please provide your email")
            return
        if is_empty(password):
            st.warning("Please provide your password")
            return
        try:
            user = auth_service.signup(email, password)
            st.session_state.user = user
            st.rerun()
        except Exception as e:
            st.error(extract_error_message(str(e)))
