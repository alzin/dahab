
class AuthService:
    def __init__(self, auth, cookie):
        self.auth = auth
        self.cookie = cookie

    def sign_in(self, email, password):
        user = self.auth.sign_in_with_email_and_password(email, password)
        self.cookie.set("refreshToken", user['refreshToken'])
        return user

    def sing_up(self, email, password):
        user = self.auth.create_user_with_email_and_password(email, password)
        self.cookie.set("refreshToken", user['refreshToken'])
        # self.auth.send_email_verification(user['idToken'])
        return user

    def validate_token(self):
        try:
            token = self.cookie.get("refreshToken")
            return self.auth.refresh(token)
        except Exception:
            return None

    def sign_out(self):
        self.cookie.delete("refreshToken")
