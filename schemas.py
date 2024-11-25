from pydantic import BaseModel

class ItemCreate(BaseModel):
    title: str
    description: str

class AdminCreate(BaseModel):
    username: str
    password: str

class AdminLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

