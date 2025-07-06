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
    
    # Add the person and get the person ID
    person_id = PersonService.add_person(first_name, last_name, birth_date, gender)
    
    # Process addresses
    form_data = await request.form()
    address_index = 0
    while f"address_line1_{address_index}" in form_data:
        address_line1 = form_data.get(f"address_line1_{address_index}")
        if address_line1 and address_line1.strip():  # Only add if address line 1 is not empty
            address_type = form_data.get(f"address_type_{address_index}", "Home")
            address_line2 = form_data.get(f"address_line2_{address_index}", "")
            city = form_data.get(f"city_{address_index}", "")
            state = form_data.get(f"state_{address_index}", "")
            postal_code = form_data.get(f"postal_code_{address_index}", "")
            country = form_data.get(f"country_{address_index}", "")
            
            PersonService.add_address(person_id, address_type, address_line1, address_line2, city, state, postal_code, country)
        address_index += 1
    
    # Process contact information
    contact_index = 0
    while f"contact_value_{contact_index}" in form_data:
        contact_value = form_data.get(f"contact_value_{contact_index}")
        if contact_value and contact_value.strip():  # Only add if contact value is not empty
            contact_type = form_data.get(f"contact_type_{contact_index}", "Phone")
            PersonService.add_contact(person_id, contact_type, contact_value)
        contact_index += 1
    
    # Redirect to the person details page
    return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)

@router.get("/manage/personal_info/edit/{person_id}", response_class=HTMLResponse)
async def edit_person_form(request: Request, person_id: int, return_to: str = Query("/manage/personal_info")):
    admin_required(request)
    person = PersonService.get_person(person_id)
    return templates.TemplateResponse("person_edit.html", {"request": request, "person": person, "return_to": return_to})

@router.post("/manage/personal_info/edit/{person_id}")
async def edit_person(request: Request, person_id: int, first_name: str = Form(...), last_name: str = Form(...), birth_date: str = Form(...), gender: str = Form(...), return_to: str = Form("/manage/personal_info")):
    admin_required(request)
    PersonService.update_person(person_id, first_name, last_name, birth_date, gender)
    return RedirectResponse(url=return_to, status_code=303)

@router.post("/manage/personal_info/delete/{person_id}")
async def delete_person(request: Request, person_id: int):
    admin_required(request)
    PersonService.delete_person(person_id)
    return RedirectResponse(url="/manage/personal_info", status_code=303)

# Address management routes
@router.post("/manage/person/{person_id}/address/add")
async def add_address(request: Request, person_id: int, address_type: str = Form(...), address_line1: str = Form(...), address_line2: str = Form(""), city: str = Form(""), state: str = Form(""), postal_code: str = Form(""), country: str = Form("")):
    admin_required(request)
    PersonService.add_address(person_id, address_type, address_line1, address_line2, city, state, postal_code, country)
    return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)

@router.post("/manage/person/{person_id}/address/{address_id}/edit")
async def edit_address(request: Request, person_id: int, address_id: int, address_type: str = Form(...), address_line1: str = Form(...), address_line2: str = Form(""), city: str = Form(""), state: str = Form(""), postal_code: str = Form(""), country: str = Form("")):
    admin_required(request)
    PersonService.update_address(address_id, address_type, address_line1, address_line2, city, state, postal_code, country)
    return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)

@router.post("/manage/person/{person_id}/address/{address_id}/delete")
async def delete_address(request: Request, person_id: int, address_id: int):
    admin_required(request)
    PersonService.delete_address(address_id)
    return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)

# Contact management routes
@router.post("/manage/person/{person_id}/contact/add")
async def add_contact(request: Request, person_id: int, contact_type: str = Form(...), contact_value: str = Form(...)):
    admin_required(request)
    PersonService.add_contact(person_id, contact_type, contact_value)
    return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)

@router.post("/manage/person/{person_id}/contact/{contact_id}/edit")
async def edit_contact(request: Request, person_id: int, contact_id: int, contact_type: str = Form(...), contact_value: str = Form(...)):
    admin_required(request)
    PersonService.update_contact(contact_id, contact_type, contact_value)
    return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)

@router.post("/manage/person/{person_id}/contact/{contact_id}/delete")
async def delete_contact(request: Request, person_id: int, contact_id: int):
    admin_required(request)
    PersonService.delete_contact(contact_id)
    return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)

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
    contacts = PersonService.get_contacts(person_id)
    roles = PersonService.get_roles(person_id)
    return templates.TemplateResponse(
        "person_details.html",
        {
            "request": request,
            "person": person,
            "addresses": addresses,
            "contacts": contacts,
            "roles": roles,
        }
    )