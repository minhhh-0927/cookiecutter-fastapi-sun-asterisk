from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

router = APIRouter(prefix="/healthy_check")


@router.get("/")
async def healthy_check():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            err_status=False
        )
    )
