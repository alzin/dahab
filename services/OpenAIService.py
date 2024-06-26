import os
import time
import streamlit as st
from openai import OpenAI


class OpenAIService:
    def __init__(self):
        self.openai = OpenAI(api_key=st.session_state.openai_api_key)

    def create_thread(self):
        try:
            return self.openai.beta.threads.create()
        except Exception as e:
            st.error(f"Error creating thread: {e}")
            return None

    def submit_message_to_thread(self, thread_id, content, assistant_id):
        self.openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )
        return self.openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

    def wait_for_response(self, thread_id, run_id):
        run = self.openai.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        while run.status == "queued" or run.status == "in_progress":
            run = self.openai.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )
            time.sleep(1)

    def get_response(self, thread_id):
        return self.openai.beta.threads.messages.list(thread_id=thread_id)
