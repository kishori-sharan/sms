from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

import mysql.connector
import hashlib
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Already loads .env

SESSION_SECRET_KEY = os.getenv("WEB_SESSION_SECRET_KEY", "default_secret")
SESSION_TIMEOUT = int(os.getenv("WEB_SESSION_TIMEOUT", "3600"))

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    max_age=SESSION_TIMEOUT
)

class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

app.add_middleware(NoCacheMiddleware)

BASE_DIR = Path(__file__).resolve().parent

# 1. Mount static/ with name="static"
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def get_db_connection():
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    # print(f"Inside get_db_connection()")
    try:
        connection = mysql.connector.connect(
                        host=host,
                        user=user,
                        password=password,
                        database=database,
                        use_pure=True,          # Important
                        connection_timeout=5
                    )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    request.session.clear()  # Clear session on login page load
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), role: str = Form("Student")):
    print(f"Received login request for username: {username}")

    salted_password = hashlib.sha256((password + username + "_salt").encode()).hexdigest()

    print(f"Before get_db_connection")
    conn = get_db_connection()
    print(f"After get_db_connection")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT users.id FROM users
        JOIN user_roles ON users.id = user_roles.user_id
        JOIN roles ON roles.id = user_roles.role_id
        WHERE users.username=%s AND users.salted_password=%s AND roles.name=%s
    ''', (username, salted_password, role))

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        # Start session
        request.session["user_id"] = user[0]
        request.session["username"] = username
        request.session["role"] = role
        return RedirectResponse(url="/home", status_code=303)
    return RedirectResponse(url="/", status_code=303)

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.api_route("/logout", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

