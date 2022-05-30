from typing import Optional, Callable

from fastapi import Request
from pydantic import BaseModel, ValidationError

from config.settings import settings
from framework.exceptions import InternalServerError, BadRequest
from framework.pagination import get_has_more


class ApiResponse:
    def __init__(self,
                 request: Request,
                 request_schema: BaseModel(),
                 response_schema: BaseModel(),
                 method: Callable[[object, Optional[str]], object],
                 body: Optional[BaseModel] = None,
                 file: Optional[any] = None,
                 is_paging: bool = None):
        self.request = request
        self.request_schema = request_schema
        self.response_schema = response_schema
        self.method = method
        self.is_paging = is_paging
        self.body = body
        self.file = file

    async def execute(self):
        req_obj, req_err = await self._request_schema_method()
        if req_err:
            raise InternalServerError(
                err_code=settings.ERROR_CODE["system"]["E0100"]["value"],
                err_msg=settings.ERROR_CODE["system"]["E0100"]["description"]
            )
        data = await self._response_schema_method(req_obj, self.method)
        return data

    async def _request_schema_method(self):
        if not self.request:
            raise BadRequest(
                err_code=settings.ERROR_CODE["system"]["E0200"]["value"],
                err_msg=settings.ERROR_CODE["system"]["E0200"]["description"]
            )

        # Handler with method POST
        if self.body and not self.request.path_params:
            self.req_obj = self.body.copy()
            return self.req_obj, None

        request_param = {}

        # Handler with request file
        if self.file:
            self.file_contents = await self.file.read()
            request_param |= dict(filename=self.file.filename, filesize=float(len(self.file_contents)))


        # Handler with method PUT
        if self.body and self.request.path_params:
            request_param |= self.body.dict()
            params = self._convert_querydict_to_dict(self.request.path_params)
            request_param.update(params)

        # Handler with method GET
        if not self.body and self.request.query_params:
            params = self._convert_querydict_to_dict(self.request.query_params)
            request_param.update(params)

        if not self.body and self.request.path_params:
            params = self._convert_querydict_to_dict(self.request.path_params)
            request_param |= params

        try:
            self.req_obj = self.request_schema(**request_param)
        except ValidationError as e:
            return {}, e.json()
        return self.req_obj, None

    def _convert_querydict_to_dict(self, querydict):
        converted_dict = {}
        for key, value in querydict.items():
            splited_item = value.split(',')
            if len(splited_item) == 1:
                converted_dict[key] = splited_item[0]
            else:
                converted_dict[key] = splited_item
        return converted_dict

    async def _response_schema_method(self, req_obj, method):
        try:
            query_set = await method(req_obj, self.file_contents) if self.file else await method(req_obj)

            if self.is_paging and not self.body:
                query_set.has_more = get_has_more(limit=self.req_obj.limit,
                                                  offset=self.req_obj.offset,
                                                  total_count=int(query_set.total_count))
        except Exception as e:
            raise e
        return query_set
