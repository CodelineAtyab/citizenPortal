from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    contact_no: str