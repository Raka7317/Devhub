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
from slowapi import _rate_limit_exceeded_handler
from app.api.routes.uploads import router as uploads_router
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response



app = FastAPI(
    title="DevHub API",
    description="Developer platform API built with FastAPI",
    version="1.0.0"
)

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

@app.get("/")
def home():
    return {
        "message": "Welcome to DevHub API"
    }


app.include_router(users_router)
app.include_router(projects_router)
app.include_router(auth_router)
app.include_router(uploads_router)