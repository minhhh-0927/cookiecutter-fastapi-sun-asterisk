from pydantic import BaseModel

from components.core.schemas import (
    Token,
)


class LoginRequestSchema(BaseModel):
    email: str
    password: str


class LoginResponseSchema(Token):
    pass
