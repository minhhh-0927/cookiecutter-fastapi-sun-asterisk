import inspect
from datetime import datetime
from functools import wraps
from typing import Callable, Type, TypeVar, List, get_type_hints, Any, Union

from fastapi import APIRouter, Depends
from loguru import logger
from pydantic.typing import is_classvar
from starlette.routing import Route, WebSocketRoute

from components.users.repositories import UserRepositories
from config.settings import settings
from framework.dependencies.jwt_bearer import decode_access_token
from framework.exceptions import *
from utilities import correlation_id

T = TypeVar("T")
CBV_CLASS_KEY = "__cbv_class__"

error_logger = logger.bind(name="error")


def default_api_response(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            api_response_obj = await func(*args, **kwargs)
            return await api_response_obj.execute()
        except Exception as e:
            error_logger.exception(e)
            if isinstance(e, BadRequest) or \
                    isinstance(e, Unauthorized) or \
                    isinstance(e, PermissionDenied) or \
                    isinstance(e, NotFound) or \
                    isinstance(e, UnprocessableEntity) or \
                    isinstance(e, InternalServerError):
                return JSONResponse(
                    status_code=e.status_code,
                    content=dict(
                        correlation_id=correlation_id.get(),
                        err_mgs=e.err_msg,
                        err_code=e.err_code
                    )
                )

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=dict(
                    correlation_id=correlation_id.get(),
                    err_mgs=settings.ERROR_CODE["system"]["E0300"]["description"],
                    err_code=settings.ERROR_CODE["system"]["E0300"]["value"]
                )
            )

    return wrapper


def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        headers = kwargs["request"].headers
        token = next((item[1].split(" ")[1] for item in headers.items() if "authorization" in item[0]), None)

        if not token:
            return __return_unauth_res()

        token_data = await decode_access_token(token)
        if token_data["exp"] <= int(datetime.now().timestamp()):
            return __return_unauth_res()
        user = await UserRepositories(kwargs["request"].state.db).is_user_exists(token_data["sub"])
        if user:
            return await func(*args, **kwargs)
        return __return_unauth_res()

    return wrapper


def __return_unauth_res():
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=dict(
            correlation_id=correlation_id.get(),
            err_mgs=settings.ERROR_CODE["auth"]["E1401"]["description"],
            err_code=settings.ERROR_CODE["auth"]["E1401"]["value"]
        )
    )


def classview(router: APIRouter) -> Callable[[Type[T]], Type[T]]:
    """
    This function returns a decorator that converts the decorated into a class-based view for the provided router.
    Any methods of the decorated class that are decorated as endpoints using the router provided to this function
    will become endpoints in the router. The first positional argument to the methods (typically `self`)
    will be populated with an instance created using FastAPI's dependency-injection.
    For more detail, review the documentation at
    https://fastapi-utils.davidmontague.xyz/user-guide/class-based-views/#the-cbv-decorator
    """

    def decorator(cls: Type[T]) -> Type[T]:
        return _classbaseview(router, cls)

    return decorator


def _classbaseview(router: APIRouter, cls: Type[T]) -> Type[T]:
    """
    Replaces any methods of the provided class `cls` that are endpoints of routes in `router` with updated
    function calls that will properly inject an instance of `cls`.
    """
    _init_cbv(cls)
    cbv_router = APIRouter(prefix=router.prefix)
    function_members = inspect.getmembers(cls, inspect.isfunction)
    functions_set = {func for _, func in function_members}
    cbv_routes = [
        route
        for route in router.routes
        if isinstance(route, (Route, WebSocketRoute)) and route.endpoint in functions_set
    ]
    for route in cbv_routes:
        router.routes.remove(route)
        _update_cbv_route_endpoint_signature(cls, route)
        cbv_router.routes.append(route)

    router.prefix = ""
    router.include_router(cbv_router)
    router.prefix = cbv_router.prefix
    return cls


def _init_cbv(cls: Type[Any]) -> None:
    """
    Idempotently modifies the provided `cls`, performing the following modifications:
    * The `__init__` function is updated to set any class-annotated dependencies as instance attributes
    * The `__signature__` attribute is updated to indicate to FastAPI what arguments should be passed to the initializer
    """
    if getattr(cls, CBV_CLASS_KEY, False):  # pragma: no cover
        return  # Already initialized
    old_init: Callable[..., Any] = cls.__init__
    old_signature = inspect.signature(old_init)
    old_parameters = list(old_signature.parameters.values())[1:]  # drop `self` parameter
    new_parameters = [
        x for x in old_parameters if x.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
    ]
    dependency_names: List[str] = []
    for name, hint in get_type_hints(cls).items():
        if is_classvar(hint):
            continue
        parameter_kwargs = {"default": getattr(cls, name, Ellipsis)}
        dependency_names.append(name)
        new_parameters.append(
            inspect.Parameter(name=name, kind=inspect.Parameter.KEYWORD_ONLY, annotation=hint, **parameter_kwargs)
        )
    new_signature = old_signature.replace(parameters=new_parameters)

    def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
        for dep_name in dependency_names:
            dep_value = kwargs.pop(dep_name)
            setattr(self, dep_name, dep_value)
        old_init(self, *args, **kwargs)

    setattr(cls, "__signature__", new_signature)
    setattr(cls, "__init__", new_init)
    setattr(cls, CBV_CLASS_KEY, True)


def _update_cbv_route_endpoint_signature(cls: Type[Any], route: Union[Route, WebSocketRoute]) -> None:
    """
    Fixes the endpoint signature for a cbv route to ensure FastAPI performs dependency injection properly.
    """
    old_endpoint = route.endpoint
    old_signature = inspect.signature(old_endpoint)
    old_parameters: List[inspect.Parameter] = list(old_signature.parameters.values())
    old_first_parameter = old_parameters[0]
    new_first_parameter = old_first_parameter.replace(default=Depends(cls))
    new_parameters = [new_first_parameter] + [
        parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY) for parameter in old_parameters[1:]
    ]
    new_signature = old_signature.replace(parameters=new_parameters)
    setattr(route.endpoint, "__signature__", new_signature)
