import datetime


class DatabaseService:
    def __init__(self, db):
        self.db = db

    def save_project(self, user_id, project_name, requirements, content, created_at, thread_id, assistant_id):
        project_data = {
            "project_name": project_name,
            "requirements": requirements,
            "content": content,
            "created_at": created_at,
            "thread_id": thread_id,
            "assistant_id": assistant_id
        }
        self.db.child("projects").child(user_id).push(project_data)

    def get_projects(self, user_id):
        return self.db.child("projects").child(user_id).get()

    def save_user_name_email(self, id, name, email):
        user_data = {
            "user_id": id,
            "name": name,
            "email": email,
            "created_at": datetime.datetime.now().isoformat()
        }
        self.db.child("users").push(user_data)
