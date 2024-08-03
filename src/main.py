from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse

from router.main import api_router
from src.exceptions.unicorn_exception import UnicornException

app = FastAPI()

app.include_router(api_router)


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exception: UnicornException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={
            "message": f"Oops! {exception.name} did something. There goes a rainbow..."
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exception: HTTPException):
    print(f"OMG! An HTTP error!: {repr(exception)}")

    # return await http_exception_handler(request, exception)
    return PlainTextResponse(str(exception.detail), status_code=exception.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
):
    print(f"OMG! The client sent invalid data!: {exception}")

    # return await request_validation_exception_handler(request, exception)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"detail": exception.errors(), "body": exception.body}
        ),
    )
