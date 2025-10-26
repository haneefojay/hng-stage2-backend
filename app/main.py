from fastapi import FastAPI, Request
from fastapi import FastAPI
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from fastapi.responses import JSONResponse
from app.routes.countries import router as countries_router
from app.routes.status import router as status_router
from app.routes.image import router as image_router
from app.database import Base, engine
from app.utils.errors import APIError

app = FastAPI(title="HNG Stage 2 Backend Task")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    # exc.detail is already a dict like {"error": ..., "details": ...}
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


@app.exception_handler(FastAPIHTTPException)
async def fastapi_http_exception_handler(request: Request, exc: FastAPIHTTPException):
    # Normalize FastAPI's HTTPException to our error format
    detail = exc.detail
    if isinstance(detail, str):
        content = {"error": detail}
    elif isinstance(detail, dict):
        content = detail
    else:
        content = {"error": "HTTP error"}
    return JSONResponse(status_code=exc.status_code, content=content)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "Internal server error"})


app.include_router(countries_router, prefix="/countries")
app.include_router(status_router)
app.include_router(image_router)
