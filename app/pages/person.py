from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.services.person_service import PersonService

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def admin_required(request: Request):
    if request.session.get("role") != "Administrator":
        return RedirectResponse(url="/", status_code=303)

@router.get("/manage/personal_info", response_class=HTMLResponse)
async def list_persons(request: Request):
    admin_required(request)
    persons = PersonService.list_persons()
    return templates.TemplateResponse("person_list.html", {"request": request, "persons": persons})

@router.get("/manage/personal_info/add", response_class=HTMLResponse)
async def add_person_form(request: Request):
    admin_required(request)
    return templates.TemplateResponse("person_add.html", {"request": request})

@router.post("/manage/personal_info/add")
async def add_person(request: Request, first_name: str = Form(...), last_name: str = Form(...), birth_date: str = Form(...), gender: str = Form(...)):
    admin_required(request)
    PersonService.add_person(first_name, last_name, birth_date, gender)
    return RedirectResponse(url="/manage/personal_info", status_code=303)

@router.get("/manage/personal_info/edit/{person_id}", response_class=HTMLResponse)
async def edit_person_form(request: Request, person_id: int):
    admin_required(request)
    person = PersonService.get_person(person_id)
    return templates.TemplateResponse("person_edit.html", {"request": request, "person": person})

@router.post("/manage/personal_info/edit/{person_id}")
async def edit_person(request: Request, person_id: int, first_name: str = Form(...), last_name: str = Form(...), birth_date: str = Form(...), gender: str = Form(...)):
    admin_required(request)
    PersonService.update_person(person_id, first_name, last_name, birth_date, gender)
    return RedirectResponse(url="/manage/personal_info", status_code=303)

@router.post("/manage/personal_info/delete/{person_id}")
async def delete_person(request: Request, person_id: int):
    admin_required(request)
    PersonService.delete_person(person_id)
    return RedirectResponse(url="/manage/personal_info", status_code=303)

# Address and contact management (add/edit/delete) can be added similarly