from fastapi import APIRouter, HTTPException
from models.user_models import User, User_patch
from services.authentication import Authentication

user_router = APIRouter(prefix="/practice_apis")

user_list = [
	{
		"id": 1,
		"name": "홍길동",
		"age": 24,
		"email": "gildong24@example.com",
		"password": "Password1234!!"
	},
	{
		"id": 2,
		"name": "장문복",
		"age": 21,
		"email": "moonluck12@example.com",
		"password": "Check1321!"
	},
	{
		"id": 3,
		"name": "임우진",
		"age": 31,
		"email": "limousine33@example.com",
		"password": "lwsPAssword12@"
	}
]

@user_router.get("/users", description="전체 회원 조회")
def get_users() -> list:
    return user_list

@user_router.get("/users/{user_id}", description="단일 유저 검색")
def get_user(user_id: int) -> dict:
    for i in range(len(user_list)):
        if user_list[i]["id"] == user_id:
            return user_list[i]
        
@user_router.post("/users", description="회원 생성")
def create_user(user: User) -> None:
    try:
        authentication = Authentication(user.email, user.password)
        authentication.email_authentication(user_list)
        authentication.password_authentication()
        idx = user_list[-1]["id"] + 1
        add_user = {
                "id": idx,
                "name": user.name,
                "age": user.age,
                "email": user.email,
                "password": user.password
			}
        user_list.append(add_user)
        return {"message": "회원가입 성공", "user": add_user}
		
    except Exception as e:
        raise HTTPException(f"오류가 발생했습니다. {e}")
    

@user_router.patch("/users/{user_id}", description="회원 수정")
def patch_user(user_id: int, user: User_patch):
    try:
        for i in range(len(user_list)):
            if user_list[i]["id"] == user_id:
                if user_list[i]["age"] != user.age:
                    user_list[i]["age"] = user.age
                authentication = Authentication(user.email, user.password)
                if user_list[i]["email"] != user.email:
                    authentication.email_authentication(user_list)
                    user_list[i]["email"] = user.email
                if user_list[i]["password"] != user.password:
                    authentication.password_authentication()
                    user_list[i]["password"] = user.password
                
                return {"message": "회원수정 성공", "user": user_id}
        raise ValueError(f"회원을 찾을 수 없습니다. {user_id}")
    except Exception as e:
        raise HTTPException(f"회원을 수정할 수 없습니다.{e}")

@user_router.delete("/users/{user_id}", description="회원 삭제")
def delete_user(user_id: int):
    try:
        for i in range(len(user_list)):
            if user_list[i]["id"] == user_id:
                del user_list[i]
                return {"message": f"{user_id}를 성공적으로 제거하였습니다.", "user_id": user_id}
        raise ValueError(f"{user_id} 회원 정보를 찾을 수 없습니다.")
            
    except Exception as e:
        raise HTTPException(f"회원정보를 삭제하지 못하였습니다. {e}")