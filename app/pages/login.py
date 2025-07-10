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
    if request.session.get("user_id"):
        return RedirectResponse(url="/home", status_code=303)
    request.session.clear()
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), role: str = Form("Student")):
    user = AuthService.login(username, password, role)
    if user:
        request.session["user_id"] = user["id"]
        request.session["username"] = user["username"]
        request.session["role"] = user["role"]
        request.session["first_name"] = user["first_name"]
        request.session["last_name"] = user["last_name"]
        return RedirectResponse(url="/home", status_code=303)
    # If login fails, show error on login page with form values preserved
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request, 
            "error": "Invalid username, password, role, or your account is deactivated. Please try again or contact admin.",
            "username": username,
            "role": role
        }
    )

@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    request.session.clear()
    return templates.TemplateResponse("logout.html", {"request": request})