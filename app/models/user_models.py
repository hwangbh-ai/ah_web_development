from pydantic import BaseModel, Field, EmailStr, PositiveInt

class User(BaseModel):
    name: str = Field(min_length=2, max_length=10)
    age: PositiveInt = Field(ge=14)
    email: EmailStr = Field(max_length=30)
    password: str = Field(min_length=8, max_length=20)

class User_patch(BaseModel):
    age: PositiveInt = Field(ge=14)
    email: EmailStr = Field(max_length=30)
    password: str = Field(min_length=8, max_length=20)