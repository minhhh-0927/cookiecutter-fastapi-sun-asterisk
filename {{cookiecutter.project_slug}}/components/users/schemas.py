from typing import Optional, List

from pydantic import BaseModel

from components.core.schemas import (
    PagingResponseSchema, PagingRequestSchema,
)


class UserBaseModel(BaseModel):
    email: Optional[str]
    id: int
    is_active: bool


class UserCreateRequestSchema(BaseModel):
    email: str
    password: str


class UserCreateResponseSchema(UserBaseModel):
    class Config:
        orm_mode = True


class UserUpdateRequestSchema(BaseModel):
    user_id: Optional[int]
    email: Optional[str]
    password: Optional[str]


class UserUpdateResponseSchema(UserBaseModel):
    class Config:
        orm_mode = True


class UserGetRequestSchema(BaseModel):
    user_id: Optional[int]


class UserGetResponseSchema(UserBaseModel):
    class Config:
        orm_mode = True


class UsersGetRequestSchema(PagingRequestSchema):
    email: Optional[str]
    user_id: Optional[str]


class UsersGetResponseSchema(PagingResponseSchema):
    data: List[UserBaseModel]
