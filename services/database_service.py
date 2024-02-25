
class DatabaseService:
    def __init__(self, db):
        self.db = db

    def save_project(self, user_id, project_name, requirements, content, created_at):
        project_data = {
            "user_id": user_id,
            "project_name": project_name,
            "requirements": requirements,
            "content": content,
            "created_at": created_at
        }
        self.db.child("projects").child(user_id).push(project_data)

    def get_projects(self, user_id):
        return self.db.child("projects").child(user_id).get()

    def save_user_name_email(self, name, email):
        user_data = {
            "name": name,
            "email": email
        }
        self.db.child("users").push(user_data)
