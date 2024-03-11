import streamlit as st
from streamlit_option_menu import option_menu
from components.login import login_ui
from components.signup import signup_ui


def guest_ui(db_service, auth_service):

    with st.sidebar:
        page = option_menu("Menu", ["Home", "Login", "Signup"], icons=[
            'house', 'door-open', 'pencil-square'], menu_icon="cast", default_index=1)

    if page == "Home":
        st.title("Welcome to JetCode")

        custom_css = """
        <style>
            .custom-button {
                background-color: #0D1116; 
                border: 2px solid; 
                border-radius: 15px; 
                padding: 10px; 
                cursor: pointer; 
                font-weight: bold; 
                text-align: center;
                display: inline-block;
                text-decoration: none;
                color: white;
            }
            .custom-button:hover {
                background-color: #1B2938;
                border-color: #F0F6FC;
                color: #F0F6FC;
            }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
        link_html = f'<a class="custom-button" href="https://rezkaudi.github.io/JetCode/" target="_blank">JetCode</a>'
        st.markdown(link_html, unsafe_allow_html=True)

    elif page == "Login":
        login_ui(auth_service)
    else:
        signup_ui(db_service, auth_service)
