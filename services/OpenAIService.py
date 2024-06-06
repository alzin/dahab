import time
from openai import OpenAI
import streamlit as st


class OpenAIService:
    def __init__(self, api_key):
        self.openai = OpenAI(api_key=api_key, default_headers={
                             "OpenAI-Beta": "assistants=v1"})

    def create_thread(self):
        try:
            return self.openai.beta.threads.create()
        except Exception as e:
            # Convert the exception to a string to make it easier to handle
            e_str = str(e)
            err = ""
            # Attempt to find and extract the message from the error
            try:
                # Assuming the error format is consistent and can be parsed as a dictionary
                error_dict = eval(e_str.split(" - ")[1])
                message = error_dict.get('error', {}).get(
                    'message', 'Unknown error')
                print(f"Error creating thread: {message}")
                err = message
            except (SyntaxError, IndexError, ValueError):
                # Handle cases where the error string cannot be parsed as expected
                print(
                    f"Error creating thread, unable to parse error message: {e_str}")
                err = e_str
            return err

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
