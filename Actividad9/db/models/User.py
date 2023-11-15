from pydantic import BaseModel 
class User(BaseModel):
    id: str | None
    username:str
    full_name: str
    email:str
    phone: str
    disabled:bool