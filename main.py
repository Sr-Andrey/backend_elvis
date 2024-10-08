from fastapi import FastAPI,Request
import logging
from contextlib import asynccontextmanager
from logging.handlers import RotatingFileHandler
from pathlib import Path
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.exceptions import HTTPException

from app.core.config import API
from app.api.main_steps.main_steps_router import router_main


@asynccontextmanager
async def lifespan(app: FastAPI):
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    Path('logs').mkdir(mode=0o774, exist_ok=True)
    logger = logging.getLogger("uvicorn.error")
    handler = RotatingFileHandler(
        "logs/unexpected_exceptions.log",
        mode="a",
        maxBytes = 100*1024,
        backupCount = 3,
    )
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    yield


app = FastAPI(
    title="registration_at_the_workplace",
    lifespan=lifespan
)


@app.exception_handler(HTTPException)
async def error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f'{exc.detail}'}
    )


app.include_router(router_main)

if __name__ == "__main__":
    app.root_path = '/registration_at_the_workplace'
    uvicorn.run(app, port=API['port'])
