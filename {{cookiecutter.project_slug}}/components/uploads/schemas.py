from pydantic import BaseModel

from components.core.schemas import (
    FileUpload,
)


class LocalUploadRequestSchema(FileUpload):
    pass


class LocalUploadResponseSchema(FileUpload):
    filepath: str
    del_flag: bool
