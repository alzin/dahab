import streamlit as st
import streamlit_antd_components as sac


def create_software_ui():
    container = st.container(border=True)
    with container:
        st.title("Create a New Software 🚀")
        user_input = st.text_area(
            "Please enter in details the requirements for your software:",
            height=300,
            key="user_input",
            help="Please detail your requirements as clearly as possible."
        )
        if st.button("Start", type="primary"):
            if not st.session_state.openai_api_key:
                st.error("Please enter your OpenAI API key.")
                return
            if not user_input:
                st.error("Please enter your requirements.")
                return
            st.session_state.requirements = user_input
            st.session_state.form_submitted = True
