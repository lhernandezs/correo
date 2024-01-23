from pydantic import BaseModel, EmailStr

class Instructor(BaseModel):
    instructor: str
    email: EmailStr
    fichas: list
