import os
import json
import re
import datetime
import streamlit as st
import extra_streamlit_components as stx

from components.guest import guest_ui
from components.create_software_ui import create_software_ui
from components.qa import qa
from components.logout import logout
from components.markdown_to_pdf_ui import MarkdownToPDFUI
from components.project_selection_ui import fetch_and_display_projects

from services.OpenAIService import OpenAIService
from authentication.auth import AuthService
from services.database_service import DatabaseService
from config.firbase_config import FirebaseService
from util.css_loader import apply_css
from util.initialize_session_state import initialize_session_state
from util.initialize_session_state import reset_session_state

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

openai = OpenAIService(OPENAI_API_KEY)
firebase_service = FirebaseService()
cookie = stx.CookieManager()
auth_service = AuthService(firebase_service.auth, cookie)
db_service = DatabaseService(firebase_service.db)

next_work_container = st.container(border=True)


def init_thread():
    if not st.session_state.thread:
        st.session_state.thread = openai.create_thread()


def thread_id():
    return st.session_state.thread.id


def is_null_or_wait(next_work):
    """
    Checks if the next work is either 'null', 'WAIT', or 'wait'.
    """
    next_work_lower = next_work.strip().lower()
    return next_work_lower == "null" or "wait" in next_work_lower


def display_next_work(next_work):
    print(next_work)
    next_work_container.write(next_work)
    next_work_container.divider()


def extract_next_work_and_content(messages):
    data = json.loads(messages.model_dump_json())
    content = data["data"][0]["content"][0]["text"]["value"]
    next_work = content.split("Next Work:")[-1].strip()
    implementation_content = content.split("Next Work:")[0].strip() + "\n"
    return next_work, implementation_content


def process_thread_interaction(initial_data):
    """
    Processes interaction with the thread based on the initial data provided,
    handles the logic to continue processing based on responses.
    """
    run = openai.submit_message_to_thread(
        thread_id(),
        initial_data,
        os.getenv("ASSISTANT_ID", ASSISTANT_ID)
    )
    openai.wait_for_response(thread_id(), run.id)
    messages = openai.get_response(thread_id())
    next_work, content = extract_next_work_and_content(messages)
    display_next_work(next_work)
    st.session_state.content += content
    return next_work


def continue_processing(next_work):
    """
    Continues processing based on the next work item.
    """
    print("Continuing processing")
    while not is_null_or_wait(next_work):
        next_work = process_thread_interaction(next_work)


def process_after_getting_answers():
    """
    Starts processing after getting initial answers, setting up any required state.
    """
    st.session_state.show_questions = False
    with st.spinner("Working on the software..."):
        next_work = process_thread_interaction(st.session_state.qa_pairs)
        continue_processing(next_work)
    st.rerun()


def extract_questions(content):
    st.session_state.questions = [line.strip() for line in content.split('\n')
                                  if re.match(r'Q\d+\:', line.strip())]


def process_requirements():
    """
    Processes initial requirements and decides the flow based on the presence of questions.
    """
    with st.spinner("Processing requirements..."):
        init_thread()
        next_work = process_thread_interaction(st.session_state.requirements)

        if is_null_or_wait(next_work):
            st.session_state.show_questions = True
            extract_questions(st.session_state.content)
            st.rerun()
        else:
            print("No questions, no wait")


def save_project():
    if not st.session_state.saved:
        st.session_state.saved = True
        created_at = datetime.datetime.now().isoformat()

        db_service.save_project(
            st.session_state.user["userId"],
            created_at,
            st.session_state.requirements,
            st.session_state.content,
            created_at=created_at
        )
        st.balloons()


def display_generated_content():
    content_container = st.container(border=True)
    content_container.write(st.session_state.content)


def display_pdf(data):
    pdf = MarkdownToPDFUI.convert_to_pdf(data)
    MarkdownToPDFUI.present(pdf)


def get_project_detail(attr):
    return st.session_state.proeject_details[st.session_state.selected_project][attr]


def show_selected_project():
    container = st.container(border=True)
    container.title(get_project_detail("project_name"))
    container.divider()
    container.header("Requirements:")
    container.write(get_project_detail("requirements"))
    container.divider()
    container.write(get_project_detail("content"))


def refresh():
    st.session_state.refresh_key += 1
    st.rerun()


def create_software_button():
    if st.sidebar.button("Create Software", key="create_software"):
        reset_session_state()
        refresh()


def process_authenticated_user_flow():
    fetch_and_display_projects(db_service)
    if st.session_state.selected_project != "Select a project":
        show_selected_project()
        display_pdf(get_project_detail("content"))
        create_software_button()
    elif not st.session_state.form_submitted:
        create_software_ui()
    elif st.session_state.first_run:
        st.session_state.first_run = False
        process_requirements()
    elif st.session_state.show_questions:
        qa(st.session_state.questions, process_after_getting_answers)
    else:
        display_generated_content()
        display_pdf(st.session_state.content)
        save_project()
        create_software_button()
    logout(auth_service)


def main():
    initialize_session_state()
    apply_css("css/wave.css")

    st.session_state.user = auth_service.validate_token()
    if st.session_state.user:
        process_authenticated_user_flow()
    else:
        guest_ui(db_service, auth_service)


if __name__ == "__main__":
    main()
