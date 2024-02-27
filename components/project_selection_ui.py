import streamlit as st


def fetch_and_display_projects(db_service):
    projects = db_service.get_projects(st.session_state.user["userId"])
    if projects.each():
        project_details = {}
        options = ["Select a project"]

        for project in projects.each():
            detail = project.val()
            project_name = detail["project_name"]
            project_details[project_name] = detail
            options.append(project_name)

        st.session_state.proeject_details = project_details
        st.session_state.selected_project = st.sidebar.selectbox(
            "Projects:",
            options,
            index=st.session_state.default_index,
            key=f'selectbox_{st.session_state.refresh_key}'
        )
