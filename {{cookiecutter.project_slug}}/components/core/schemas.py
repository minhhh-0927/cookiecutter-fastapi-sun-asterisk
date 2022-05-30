from typing import Optional
from datetime import datetime

from fastapi import File
from pydantic import BaseModel


class PagingRequestSchema(BaseModel):
    limit: Optional[int]
    offset: Optional[int]
    all: Optional[bool]


class SearchPagingRequestSchema(PagingRequestSchema):
    query = str


class PagingResponseSchema(BaseModel):
    total_count: int
    has_more: Optional[bool]


class Token(BaseModel):
    token: str
    token_type: str
    expires_in: datetime


class FileUpload(BaseModel):
    filename: str
    filesize: float
