from typing import List
import re

# email, password 인증
class Authentication:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def email_authentication(self, user_list: List(dict)):
        email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, self.email):
            raise ValueError("Email형식이 다릅니다.")

        if any(self.email == other_email for other_email in user_list):
            raise ValueError("이미 존재하는 Email입니다.")
        
    def password_authentication(self):
        if not re.search(r"[A-Z]", self.password):
            raise ValueError("비밀번호에 대문자가 최소 1개 포함되어야 합니다.")
        if not re.search(r"[a-z]", self.password):
            raise ValueError("비밀번호에 소문자가 최소 1개 포함되어야 합니다.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", self.password):
            raise ValueError("비밀번호에 특수문자가 최소 1개 포함되어야 합니다.")
        