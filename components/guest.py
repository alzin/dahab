import streamlit as st
from streamlit_option_menu import option_menu
from components.login import login_ui
from components.signup import signup_ui
import webbrowser


def guest_ui(auth_service):

    with st.sidebar:
        page = option_menu("Main Menu", ["Slash Code AI", "Login", "Signup"], icons=[
            'rocket-takeoff', 'door-open', 'pencil-square'], menu_icon="cast", default_index=1)

    if page == "Slash Code AI":
        url = "https://rezkaudi.github.io/TriibeTask"
        webbrowser.open_new_tab(url)
    elif page == "Login":
        login_ui(auth_service)
    else:
        signup_ui(auth_service)
