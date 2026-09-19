from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.request_size import request_size_middleware
from app.api.routes.users import router as users_router
from app.api.routes.projects import router as projects_router
from app.api.routes.auth import router as auth_router
from app.core.exception_handlers import global_exception_handler
from app.core.rate_limit import limiter
from slowapi.errors import RateLimitExceeded
from app.core.performance_middleware import performance_middleware
from fastapi.staticfiles import StaticFiles
from app.api.routes.websocket import router as websocket_router
from app.api.routes.streaming import router as streaming_router
from app.api.routes.health import router as health_router
from app.api.v1.users import router as users_v1_router
from app.api.v2.users import router as users_v2_router



from contextlib import asynccontextmanager
from slowapi import _rate_limit_exceeded_handler
from app.api.routes.uploads import router as uploads_router
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 DevHub API is starting...")

    # Startup logic goes here

    yield

    # Shutdown logic goes here
    print("🛑 DevHub API is shutting down...")



app = FastAPI(
    title="DevHub API",
    description="Developer platform API built with FastAPI",
    version="1.0.0",
    lifespan=lifespan
)
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
app.include_router(websocket_router)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SecurityHeadersMiddleware)
@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    return await request_size_middleware(request, call_next)


@app.middleware("http")
async def add_process_time(
    request: Request,
    call_next
):
    return await performance_middleware(
        request,
        call_next
    )




@app.get("/")
def home():
    return {
        "message": "Welcome to DevHub API"
    }




app.include_router(users_router)
app.include_router(projects_router)
app.include_router(auth_router)
app.include_router(uploads_router)
app.include_router(streaming_router)
app.include_router(health_router)
app.include_router(users_v1_router)
app.include_router(users_v2_router)