from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.services.user_service import UserService
from app.services.person_service import PersonService

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/users", response_class=HTMLResponse)
async def user_list(request: Request):
    users = UserService.list_users()
    return templates.TemplateResponse("user_list.html", {"request": request, "users": users})

@router.get("/users/add", response_class=HTMLResponse)
async def user_add_page(request: Request):
    people = UserService.get_all_people()
    roles = UserService.get_all_roles()
    return templates.TemplateResponse("user_add.html", {"request": request, "people": people, "roles": roles})

@router.post("/users/add")
async def user_add(request: Request, username: str = Form(...), password: str = Form(...), person_id: int = Form(...), roles: list = Form(...), active: bool = Form(False)):
    UserService.add_user(username, password, person_id, [int(r) for r in roles], active)
    return RedirectResponse(url="/users", status_code=303)

@router.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def user_edit_page(request: Request, user_id: int):
    user = UserService.get_user(user_id)
    people = UserService.get_all_people()
    roles = UserService.get_all_roles()
    return templates.TemplateResponse("user_edit.html", {"request": request, "user": user, "people": people, "roles": roles})

@router.post("/users/{user_id}/edit")
async def user_edit(request: Request, user_id: int, username: str = Form(...), password: str = Form(None), person_id: int = Form(...), roles: list = Form(...), active: bool = Form(False)):
    UserService.update_user(user_id, username, password, person_id, [int(r) for r in roles], active)
    return RedirectResponse(url="/users", status_code=303)

@router.post("/users/{user_id}/delete")
async def user_delete(request: Request, user_id: int):
    UserService.delete_user(user_id)
    return RedirectResponse(url="/users", status_code=303)

@router.post("/users/{user_id}/toggle_active")
async def user_toggle_active(request: Request, user_id: int, active: bool = Form(...)):
    UserService.toggle_active(user_id, active)
    return RedirectResponse(url="/users", status_code=303)

@router.get("/user_search", response_class=HTMLResponse)
async def user_search_form(request: Request):
    return templates.TemplateResponse("user_search.html", {"request": request})

@router.get("/user_search/results", response_class=HTMLResponse)
async def user_search_results(request: Request, username: str = "", role: str = "", active: str = ""):
    users = UserService.search_users(username=username, role=role, active=active)
    return templates.TemplateResponse("user_search_results.html", {"request": request, "users": users, "username": username, "role": role, "active": active}) 