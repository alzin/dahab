import streamlit as st
from components.login import login_ui
from components.signup import signup_ui


def guest_ui(auth_service):
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Please choose an option", [
                            "Home", "Login", "Signup"])
    if page == "Home":
        st.markdown(open('Home.md').read())
    elif page == "Login":
        login_ui(auth_service)
    else:
        signup_ui(auth_service)
