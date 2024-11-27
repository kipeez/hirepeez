import asyncio
import time
from datetime import datetime
from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from kipeez.common.date.mocktime import mocktime
from kipeez.routes.auth import auth_router
from kipeez.routes.users import users_router
from kipeez.routes.organisations import organisations_router


app = FastAPI()



origins = [
    "*",
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(organisations_router.router)


logger = logging.getLogger('uvicorn.error')
class LogTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Get client IP address (if it's behind a proxy like NGINX, use headers to extract it)
        client_ip = request.client.host

        # Build request line in Apache format
        request_line = f"{request.method} {request.url.path} {request.scope['http_version']}"

        # Get current time in the format of [day/month/year:hour:minute:second offset]
        current_time = datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S +0000")

        # Process the request and get the response
        response = await call_next(request)

        # Calculate time taken to process the request
        process_time = time.time() - start_time

        # Get response status code
        status_code = response.status_code

        # Get response content length (if set in the headers)
        content_length = response.headers.get("content-length", "-")

        # Format the log entry
        log_entry = f'{client_ip} - [{current_time}] "{request_line}" {status_code} {content_length} {process_time:.4f}s'

        # Log the request in Apache format
        logger.info(log_entry)

        return response
        
app.add_middleware(LogTimeMiddleware)

@app.get("/")
async def root():
    return {"greeting":"Hello world!"}

