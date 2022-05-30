import uuid

from fastapi import UploadFile
from loguru import logger
from sqlalchemy.orm import Session

from components.uploads.repositories import UploadRepositories
from components.uploads.schemas import (
    LocalUploadRequestSchema, LocalUploadResponseSchema
)
from config.settings import settings
from framework.exceptions import InternalServerError

error_logger = logger.bind(name="error")


class UploadLogic:

    def __init__(self, db: Session):
        self.db = db

    async def upload_file_to_local(self, request: LocalUploadRequestSchema,
                                   file_content: bytes) -> LocalUploadResponseSchema:
        try:
            origin_filename = request.filename
            uuid_filename = f"{uuid.uuid4()}{origin_filename}"
            filepath = f"upload/{uuid_filename}"
            with open(filepath, 'wb') as f:
                f.write(file_content)
        except Exception as e:
            logger.exception(e)
            raise InternalServerError(
                err_code=settings.ERROR_CODE["system"]["E0100"]["value"],
                err_msg=settings.ERROR_CODE["system"]["E0100"]["description"]
            )

        file_upload = await UploadRepositories(self.db).create_local_file(
            filename=origin_filename,
            filesize=request.filesize,
            filepath=uuid_filename
        )
        return LocalUploadResponseSchema(filename=file_upload.filename,
                                         filesize=file_upload.filesize,
                                         filepath=file_upload.filepath,
                                         del_flag=file_upload.del_flag)
