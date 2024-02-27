import streamlit as st


def initialize_session_state():
    """Initialize Streamlit session state with default values."""
    defaults = {
        "projects": None,
        "requirements": "",
        "form_submitted": False,
        "first_run": True,
        "show_questions": True,
        "content": "",
        "questions": None,
        "thread": None,
        "qa_pairs": "",
        "current_question_index": 0,
        "responses": [],
        "submitted_all": False,
        "default_index": 0,
        "selected_project": "Select a project",
        "saved": False,
        "proeject_details": {},
        "default_index": 0,
        "refresh_key": 0,
        "project_name": "",
        "show_next_work": False,
    }
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
            # st.write(f"Resetting {key} to {default_value}")


def reset_session_state():
    """Reset Streamlit session state variables to their default values."""
    defaults = {
        "projects": None,
        "requirements": "",
        "form_submitted": False,
        "first_run": True,
        "show_questions": True,
        "content": "",
        "questions": None,
        "thread": None,
        "qa_pairs": "",
        "current_question_index": 0,
        "responses": [],
        "submitted_all": False,
        "default_index": 0,
        "selected_project": "Select a project",
        "saved": False,
        "proeject_details": {},
        "default_index": 0,
        "project_name": "",
        "show_next_work": False,
    }
    for key, default_value in defaults.items():
        st.session_state[key] = default_value
