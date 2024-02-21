import streamlit as st


def logout(auth_service):
    if st.sidebar.button("Logout"):
        auth_service.sign_out()
        st.session_state.user = None
        st.session_state.requirements_submitted = False
