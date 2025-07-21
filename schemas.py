from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str 

class SubmissionRequest(BaseModel):
    content: str
