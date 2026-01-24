from contextlib import asynccontextmanager
import time
from fastapi import FastAPI, Request
import threading
import os
from datetime import datetime
import asyncio
import anyio



@asynccontextmanager
async def lifespan(app: FastAPI):
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 100
    yield
    limiter.total_tokens = 40

app = FastAPI(lifespan=lifespan)


def custom_log(message=""):
    thread = threading.current_thread()
    thread_id = thread.ident
    thread_name = thread.name
    pid = os.getpid()
    now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(
        f"{now}, Pid:{pid} Thread id: {thread_id}, thread_name: ${thread_name}, message: {message}"
    )


# @app.middleware("http")
# def log_request_info(request: Request, call_next):
#     custom_log("middleware call")
#     response = call_next(request)
#     return response

@app.middleware("http")
async def log_request_info(request: Request, call_next):
    custom_log("middleware call")
    response = await call_next(request)
    return response

def get_data():
    time.sleep(1)
    return {"foo": "bar"}


async def async_get_data():
    await asyncio.sleep(1)
    return {"foo": "bar"}


async def async_with_sync_get_data():
    time.sleep(1)
    return {"foo": "bar"}


@app.get("/sync-request")
def sync_request():
    custom_log("(async-request) before get_data")
    response = get_data()
    custom_log("(async-request) after get_data")
    return response


@app.get("/async-request")
async def async_request():
    custom_log("(async-request) before get_data")
    response = await async_get_data()
    custom_log("(async-request) after get_data")
    return response


@app.get("/async-with-block-request")
async def async_request_with_sync_blocker():
    custom_log("(async-with-block-request) before get_data")
    response = await async_with_sync_get_data()
    custom_log("(async-with-block-request) after get_data")
    return response
