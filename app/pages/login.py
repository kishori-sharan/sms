from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.services.auth_service import AuthService

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    request.session.clear()
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), role: str = Form("Student")):
    user = AuthService.login(username, password, role)
    if user:
        request.session["user_id"] = user["id"]
        request.session["username"] = username
        request.session["role"] = role
        return RedirectResponse(url="/home", status_code=303)
    # If login fails, show error on login page
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid username, password, or role. Please try again."}
    )

@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    request.session.clear()
    return templates.TemplateResponse("logout.html", {"request": request})