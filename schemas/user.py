from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    surname: str
    email: str
    phone: str
    photo: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
