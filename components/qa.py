import streamlit as st
from streamlit_chat import message


def qa(questions_list, func):

    # Function to handle question progression and submission
    def handle_next_question():
        user_input = st.session_state[f'user_input_{st.session_state.current_question_index}'].strip(
        )
        if user_input:
            st.session_state.responses.append(user_input)
            st.session_state.current_question_index += 1
            if st.session_state.current_question_index >= len(questions_list):
                st.session_state.submitted_all = True
        else:
            st.warning('Please provide a response before submitting.')

    # Reset/clear function
    def reset_survey():
        st.session_state.current_question_index = 0
        st.session_state.responses = []
        st.session_state.submitted_all = False
        st.session_state.qa_pairs = ""

    # Display questions and answers in a chat format
    for i in range(st.session_state.current_question_index):
        message(questions_list[i], key=f"question_{i}")
        if i < len(st.session_state.responses):
            message(st.session_state.responses[i],
                    is_user=True, key=f"response_{i}")
    if not st.session_state.submitted_all and st.session_state.current_question_index < len(questions_list):
        message(questions_list[st.session_state.current_question_index],
                key=f"current_question_{st.session_state.current_question_index}")

    # User input form - show only if not all questions have been submitted
    if not st.session_state.submitted_all:
        with st.form(key=f'response_form_{st.session_state.current_question_index}'):
            user_input = st.text_input(
                "", key=f"user_input_{st.session_state.current_question_index}")
            submit_button = st.form_submit_button(
                label='Submit', on_click=handle_next_question)

    if st.session_state.submitted_all:
        for question, response in zip(questions_list, st.session_state.responses):
            st.session_state.qa_pairs += f"{question}\n {response}\n \n "
        func()
        reset_survey()
