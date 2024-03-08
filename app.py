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

from util.initialize_session_state import initialize_session_state
from util.initialize_session_state import reset_session_state
from util.spinner import Spinner

st.set_page_config(
    page_title="JetCode",
    page_icon="🔥"
)


ASSISTANT_ID = os.getenv("ASSISTANT_ID")

initialize_session_state()

firebase_service = FirebaseService()
cookie = stx.CookieManager()
openai = OpenAIService()
auth_service = AuthService(firebase_service.auth, cookie)
db_service = DatabaseService(firebase_service.db)

placeholder = st.empty()
next_work_container = placeholder.container()


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
    with next_work_container:
        next_work_container.write("_ " + next_work)
    print(next_work)


def extract_next_work_and_content(messages):
    data = json.loads(messages.model_dump_json())
    content = data["data"][0]["content"][0]["text"]["value"]
    next_work = content.split("Next Work:")[-1].strip()
    implementation_content = content.split("Next Work:")[0].strip() + "\n"
    return next_work, implementation_content


def extract_project_title(s):
    pattern = r"Project Title: (.*?)\s*\n"
    match = re.search(pattern, s)
    if match:
        return match.group(1).strip()
    else:
        return "YOUR PROJECT DETAILS"


def process_thread_interaction(initial_data):
    run = openai.submit_message_to_thread(
        thread_id(),
        initial_data,
        os.getenv("ASSISTANT_ID", ASSISTANT_ID)
    )
    openai.wait_for_response(thread_id(), run.id)
    messages = openai.get_response(thread_id())
    next_work, content = extract_next_work_and_content(messages)
    print(content)
    display_next_work(next_work)
    st.session_state.content += content
    return next_work


def continue_processing(next_work):
    print("Continuing processing")
    while not is_null_or_wait(next_work):
        next_work = process_thread_interaction(next_work)


def process_after_getting_answers():
    Spinner.show("Please wait,<br /> Working on your requirements...")
    next_work = process_thread_interaction(st.session_state.qa_pairs)
    continue_processing(next_work)
    st.session_state.show_next_work = False
    Spinner.remove()
    st.rerun()


def extract_questions(content):
    st.session_state.questions = [line.strip() for line in content.split('\n')
                                  if re.match(r'Q\d+\:', line.strip())]


def process_requirements():
    """
    Processes initial requirements and decides the flow based on the presence of questions.
    """
    Spinner.show("Please wait,<br /> Working on your requirements...")
    init_thread()
    next_work = process_thread_interaction(st.session_state.requirements)
    Spinner.remove()

    if is_null_or_wait(next_work):
        print("GOT QUESTIONS")
        st.session_state.show_questions = True
        content = st.session_state.content
        print(content)
        st.session_state.project_name = extract_project_title(content)
        print(st.session_state.project_name)
        extract_questions(content)
        # no need to write the questions so we need to reset the content
        st.session_state.content = ""
        st.rerun()
    else:  # if there are no questions, continue processing
        print("NO QUESTIONS")
        content = st.session_state.content
        print(content)
        st.session_state.project_name = extract_project_title(content)
        st.session_state.content += content
        print(st.session_state.project_name)
        # process the next work
        continue_processing(next_work)


def save_project():
    if not st.session_state.saved:
        st.session_state.saved = True
        created_at = datetime.datetime.now().isoformat()
        db_service.save_project(
            st.session_state.user["userId"],
            st.session_state.project_name,
            st.session_state.requirements,
            st.session_state.content,
            created_at=created_at,
            thread_id=thread_id(),
            assistant_id=ASSISTANT_ID
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
    container.header("Requirements:")
    container.write(get_project_detail("requirements"))
    container.header("Project Details")
    container.write(get_project_detail("content"))


def refresh():
    st.session_state.refresh_key += 1
    st.rerun()


def create_software_button():
    st.sidebar.markdown("---")
    if st.sidebar.button("Create Software", key="create_software"):
        reset_session_state()
        refresh()


def get_openai_api_key():
    new_key = st.sidebar.text_input(
        "OpenAI API Key: *", value=cookie.get("openai_api_key"), type="password")
    st.sidebar.markdown("---")
    if st.session_state.openai_api_key != new_key:
        st.session_state.openai_api_key = new_key
        cookie.set("openai_api_key", new_key)


def process_authenticated_user_flow():
    get_openai_api_key()
    global openai
    openai = OpenAIService()
    fetch_and_display_projects(db_service)
    if st.session_state.selected_project != "Select a project":
        show_selected_project()
        if st.button("Generate PDF"):
            display_pdf(get_project_detail("content"))
        create_software_button()
    elif not st.session_state.form_submitted:
        create_software_ui()
    elif st.session_state.first_run:
        st.session_state.first_run = False
        process_requirements()
    elif st.session_state.show_questions:
        qa(st.session_state.questions, placeholder)
    elif st.session_state.show_next_work:
        process_after_getting_answers()
    else:
        display_generated_content()
        if st.button("Generate PDF"):
            display_pdf(st.session_state.content)
        save_project()
        create_software_button()
    logout(auth_service)


def main():
    initialize_session_state()
    st.session_state.user = auth_service.validate_token()
    if st.session_state.user:
        process_authenticated_user_flow()
    else:
        guest_ui(db_service, auth_service)


if __name__ == "__main__":
    main()
