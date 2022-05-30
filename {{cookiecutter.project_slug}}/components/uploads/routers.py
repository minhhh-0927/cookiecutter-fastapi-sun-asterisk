from fastapi import APIRouter, Depends, Request, File, UploadFile
from sqlalchemy.orm import Session

from components.uploads.logics import UploadLogic
from config.settings import get_db
from framework.api_response import ApiResponse
from framework.decorators import default_api_response, classview

from components.uploads.schemas import (
    LocalUploadRequestSchema, LocalUploadResponseSchema
)

router = APIRouter(prefix="/api/v1/upload")


@classview(router)
class LocalUploadView:

    session: Session = Depends(get_db)

    @router.post("/local")
    @default_api_response
    async def local_upload(self, request: Request,
                           file: UploadFile):
        return ApiResponse(
            request=request,
            request_schema=LocalUploadRequestSchema,
            response_schema=LocalUploadResponseSchema,
            method=UploadLogic(self.session).upload_file_to_local,
            file=file
        )
