from models import RoleType

from schemas.base import UserBase


class UserRegisterIn(UserBase):
    first_name: str
    last_name: str
    password: str
    phone: str
    iban: str
    role: RoleType


class UserLoginIn(UserBase):
    password: str


