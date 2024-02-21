import os
import time
from openai import OpenAI


class OpenAIService:
    def __init__(self, api_key):
        self.openai = OpenAI(api_key=api_key)

    def create_thread(self):
        return self.openai.beta.threads.create()

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
