from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pathlib import Path
from app.pages import login, home, favicon, person, user, academic
from app.middleware.core import NoCacheMiddleware, AuthRequiredMiddleware
import os
import sys
from dotenv import load_dotenv

load_dotenv()

SESSION_SECRET_KEY = os.getenv("WEB_SESSION_SECRET_KEY", "default_secret")
SESSION_TIMEOUT = int(os.getenv("WEB_SESSION_TIMEOUT", "3600"))

app = FastAPI()

app.add_middleware(NoCacheMiddleware)
app.add_middleware(AuthRequiredMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    max_age=SESSION_TIMEOUT
)

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Import and include routers
app.include_router(login.router)
app.include_router(home.router)
app.include_router(favicon.router)
app.include_router(person.router)
app.include_router(user.router)
app.include_router(academic.router)

# Debug: print registered routes
print("\nRegistered routes:", file=sys.stderr)
for route in app.routes:
    if hasattr(route, "methods"):
        print(f"{route.path} -> {route.methods}", file=sys.stderr)
    else:
        print(f"{route.path} -> (no methods)", file=sys.stderr)
print("Running file:", os.path.abspath(__file__), file=sys.stderr)
