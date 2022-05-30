from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from components.auth.logics import AuthLogic
from config.settings import get_db
from framework.api_response import ApiResponse
from framework.decorators import default_api_response, classview

from components.auth.schemas import (
    LoginRequestSchema, LoginResponseSchema
)

router = APIRouter(prefix="/auth")


@classview(router)
class LoginView:

    session: Session = Depends(get_db)

    @router.post("/login")
    @default_api_response
    async def login(self, request: Request,
                    login: LoginRequestSchema):
        return ApiResponse(
            request=request,
            request_schema=LoginRequestSchema,
            response_schema=LoginResponseSchema,
            method=AuthLogic(self.session).login,
            body=login
        )
