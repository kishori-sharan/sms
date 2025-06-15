from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import mysql.connector
import hashlib
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Load database credentials from .env file

app = FastAPI()
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
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), role: str = Form("Student")):
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
        return RedirectResponse(url="/home", status_code=303)
    return RedirectResponse(url="/", status_code=303)

@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

