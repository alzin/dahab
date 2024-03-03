import streamlit as st
from streamlit_chat import message


def qa(questions_list, placeholder):
    placeholder = st.empty()  # Placeholder for the chat

    # Function to handle question progression and submission
    def handle_next_question():
        current_key = f'user_input_{st.session_state.current_question_index}'
        user_input = st.session_state[current_key].strip(
        ) if current_key in st.session_state else ""
        if user_input:
            st.session_state.responses.append(user_input)
            st.session_state.current_question_index += 1
            if st.session_state.current_question_index >= len(questions_list):
                st.session_state.submitted_all = True
            else:
                # Reset input for the next question
                st.session_state[current_key] = ''
        else:
            st.warning('Please provide a response before submitting.')

    # Reset/clear function
    def reset_survey():
        st.session_state.current_question_index = 0
        st.session_state.responses = []
        st.session_state.submitted_all = False
        st.session_state.qa_pairs = ""

    # Initialize session state variables if they don't exist
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'responses' not in st.session_state:
        st.session_state.responses = []
    if 'submitted_all' not in st.session_state:
        st.session_state.submitted_all = False

    # Use chat_placeholder to display questions and answers in a chat format
    with placeholder.container():
        for i in range(st.session_state.current_question_index):
            message(questions_list[i], key=f"question_{i}")
            if i < len(st.session_state.responses):
                message(st.session_state.responses[i],
                        is_user=True, key=f"response_{i}")

        if not st.session_state.submitted_all and st.session_state.current_question_index < len(questions_list):
            message(questions_list[st.session_state.current_question_index],
                    key=f"current_question_{st.session_state.current_question_index}")
            st.text_input("Answer:", key=f"user_input_{st.session_state.current_question_index}",
                          on_change=handle_next_question, label_visibility="collapsed")

    if st.session_state.submitted_all:
        for question, response in zip(questions_list, st.session_state.responses):
            st.session_state.qa_pairs += f"{question}\n {response}\n \n "
        st.session_state.show_questions = False
        st.session_state.show_next_work = True
        placeholder.empty()
        st.rerun()
        placeholder.empty()
        reset_survey()
