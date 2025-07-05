from fastapi import APIRouter, Request, Form, Depends, Query
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.services.person_service import PersonService
import os
from starlette.status import HTTP_303_SEE_OTHER

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

MAX_SEARCH_RESULTS = int(os.environ.get("MAX_SEARCH_RESULTS", 5000))

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

@router.get("/manage/person_search", response_class=HTMLResponse)
async def person_search_form(request: Request):
    admin_required(request)
    return templates.TemplateResponse("person_search.html", {"request": request})

@router.get("/manage/person_search/results", response_class=HTMLResponse)
async def person_search_results(
    request: Request,
    first_name: str = Query("", alias="first_name"),
    last_name: str = Query("", alias="last_name"),
    birth_date: str = Query("", alias="birth_date"),
    gender: str = Query("", alias="gender"),
    role: str = Query("", alias="role"),
    page: int = Query(1, alias="page"),
    page_size: int = Query(50, alias="page_size"),
    sort_by: str = Query("first_name", alias="sort_by"),
    sort_order: str = Query("asc", alias="sort_order"),
):
    admin_required(request)
    total_count = PersonService.count_persons(first_name, last_name, birth_date, gender, role)
    if total_count > MAX_SEARCH_RESULTS:
        return templates.TemplateResponse(
            "person_search.html",
            {
                "request": request,
                "error": "Too many results. Please refine your search criteria.",
                "first_name": first_name,
                "last_name": last_name,
                "birth_date": birth_date,
                "gender": gender,
                "role": role,
            },
        )
    offset = (page - 1) * page_size
    persons = PersonService.search_persons(
        first_name, last_name, birth_date, gender, role, offset, page_size, sort_by, sort_order
    )
    total_pages = (total_count + page_size - 1) // page_size
    return templates.TemplateResponse(
        "person_search_results.html",
        {
            "request": request,
            "persons": persons,
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "gender": gender,
            "role": role,
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
            "total_pages": total_pages,
            "sort_by": sort_by,
            "sort_order": sort_order,
        },
    )

@router.get("/manage/person/{person_id}", response_class=HTMLResponse)
async def person_details(request: Request, person_id: int):
    # Check if user is logged in and is Administrator
    if not request.session.get("user_id") or request.session.get("role") != "Administrator":
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    person = PersonService.get_person(person_id)
    addresses = PersonService.get_addresses(person_id)
    phones = PersonService.get_phones(person_id)
    roles = PersonService.get_roles(person_id)
    return templates.TemplateResponse(
        "person_details.html",
        {
            "request": request,
            "person": person,
            "addresses": addresses,
            "phones": phones,
            "roles": roles,
        }
    )