import streamlit as st
import streamlit_antd_components as sac


def create_software_ui():
    st.title("AI-Powered Code Generator")
    container = st.container(border=True)
    with container:
        st.subheader(
            "Generate code steps for your software requirements")
        user_input = st.text_area(
            "Describe Your Software Requirements for Any Platform:",
            height=300,
            key="user_input",
            help="Detail your software requirements for any platform, whether it's iOS, Android, web frontend, backend, or desktop applications. Specify the platform and any stack preferences (e.g., frameworks, languages) alongside desired features, functionality, and specifics of your project. The more detailed your description, the better the AI can tailor the generated code steps to your needs."
        )
        if st.button("Generate Code Steps", type="primary"):
            if not st.session_state.openai_api_key:
                st.error("Missing the OpenAI API key.")
                return
            if not user_input:
                st.error("It seems your requirements box is empty. To generate the best code steps for you, we need a bit of information about your project. Please describe your software needs, including any specific platforms like iOS, Android, Frontend, Backend, or Desktop applications you’re targeting. The more details you provide, the more tailored our AI-generated code will be to your project.")
                return
            st.session_state.requirements = user_input
            st.session_state.form_submitted = True
            st.rerun()
