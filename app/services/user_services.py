from typing import List
from models.user_models import User, User_patch

class UserServices:
    def __init__(self, user_list: List(dict)):
        self.user_list = user_list

    def create_user(self, user: User):
        idx = self.user_list[-1]["id"] + 1
        add_user = {
                "id": idx,
                "name": user.name,
                "age": user.age,
                "email": user.email,
                "password": user.password
			}
        self.user_list.append(add_user)
        return self.user_list