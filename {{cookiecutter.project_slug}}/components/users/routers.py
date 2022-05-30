from typing import Optional

from fastapi import APIRouter, Depends, Request, Query
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from components.users.logics import UserLogic
from config.settings import get_db
from framework.api_response import ApiResponse
# from framework.authentication import JWTBearer
from framework.decorators import default_api_response, classview, login_required

from components.users.schemas import (
    UsersGetRequestSchema, UsersGetResponseSchema, UserCreateRequestSchema, UserCreateResponseSchema,
    UserGetRequestSchema, UserGetResponseSchema, UserUpdateRequestSchema, UserUpdateResponseSchema,
)

router = APIRouter(
    prefix="/api/v1/users",
    dependencies=[
        # Depends(JWTBearer())
    ]
)


@classview(router)
class UserListCreateView:

    session: Session = Depends(get_db)

    @router.get("/")
    # @login_required
    @cache(expire=600)
    @default_api_response
    async def get(self, request: Request,
                  params: UsersGetRequestSchema = Depends()):
        return ApiResponse(
            request=request,
            request_schema=UsersGetRequestSchema,
            response_schema=UsersGetResponseSchema,
            method=UserLogic(self.session).get_users,
            is_paging=True
        )

    @router.post("/")
    # @login_required
    @default_api_response
    async def post(self, request: Request,
                   user: UserCreateRequestSchema):
        return ApiResponse(
            request=request,
            request_schema=UserCreateRequestSchema,
            response_schema=UserCreateResponseSchema,
            method=UserLogic(self.session).create_user,
            body=user
        )


@classview(router)
class UserUpdateRetrieveView:

    session: Session = Depends(get_db)

    @router.get("/{user_id}")
    # @login_required
    @default_api_response
    async def get(self, user_id: int,
                  request: Request):
        return ApiResponse(
            request=request,
            request_schema=UserGetRequestSchema,
            response_schema=UserGetResponseSchema,
            method=UserLogic(self.session).retrieve_user
        )

    @router.put("/{user_id}")
    # @login_required
    @default_api_response
    async def update_user(self, user_id: int,
                          request: Request,
                          user: UserUpdateRequestSchema):
        return ApiResponse(
            request=request,
            request_schema=UserUpdateRequestSchema,
            response_schema=UserUpdateResponseSchema,
            method=UserLogic(self.session).update_user,
            body=user
        )
