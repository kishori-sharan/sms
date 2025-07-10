from fastapi import APIRouter, Request, Form, Depends, Query
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.services.person_service import PersonService
import os
from starlette.status import HTTP_303_SEE_OTHER
from app.services.user_service import UserService
from app.services.db_service import DBService

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

MAX_SEARCH_RESULTS = int(os.environ.get("MAX_SEARCH_RESULTS", 5000))

def admin_required(request: Request):
    if request.session.get("role") != "Administrator":
        return RedirectResponse(url="/", status_code=303)

@router.get("/change_password", response_class=HTMLResponse)
async def change_password_form(request: Request):
    # Check if user is logged in
    if not request.session.get("user_id"):
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse("change_password.html", {"request": request})

@router.post("/change_password")
async def change_password(request: Request, current_password: str = Form(...), new_password: str = Form(...), confirm_password: str = Form(...)):
    # Check if user is logged in
    if not request.session.get("user_id"):
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    
    user_id = request.session.get("user_id")
    user = UserService.get_user(user_id)
    
    if not user:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    
    # Validate current password
    if user["password"] != current_password:
        return templates.TemplateResponse(
            "change_password.html",
            {
                "request": request,
                "error": "Current password is incorrect."
            }
        )
    
    # Validate new password confirmation
    if new_password != confirm_password:
        return templates.TemplateResponse(
            "change_password.html",
            {
                "request": request,
                "error": "New passwords do not match."
            }
        )
    
    # Update password
    UserService.update_user_password(user_id, new_password)
    
    return RedirectResponse(url="/profile?success=password_changed", status_code=303)

@router.get("/profile", response_class=HTMLResponse)
async def user_profile(request: Request):
    # Check if user is logged in
    if not request.session.get("user_id"):
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    
    # Get user details
    user_id = request.session.get("user_id")
    user = UserService.get_user(user_id)
    
    if not user:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    
    # Get person details
    person = PersonService.get_person(user["person_id"])
    addresses = PersonService.get_addresses(user["person_id"])
    contacts = PersonService.get_contacts(user["person_id"])
    
    # Get user roles
    all_roles = UserService.get_all_roles()
    conn = DBService.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT role_id FROM user_roles WHERE user_id = %s', (user_id,))
    user_role_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    
    # Check for success message
    success_message = None
    if request.query_params.get("success") == "password_changed":
        success_message = "Password changed successfully!"
    
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": user,
            "person": person,
            "addresses": addresses,
            "contacts": contacts,
            "all_roles": all_roles,
            "user_role_ids": user_role_ids,
            "success_message": success_message,
        }
    )

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
async def person_details(request: Request, person_id: int, error: str = Query(None)):
    # Check if user is logged in and is Administrator
    if not request.session.get("user_id") or request.session.get("role") != "Administrator":
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    person = PersonService.get_person(person_id)
    addresses = PersonService.get_addresses(person_id)
    contacts = PersonService.get_contacts(person_id)
    roles = PersonService.get_roles(person_id)
    user_for_person = UserService.get_user_by_person_id(person_id)
    all_roles = UserService.get_all_roles()
    user_role_ids = []
    if user_for_person:
        # Get user roles for this user
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT role_id FROM user_roles WHERE user_id = %s', (user_for_person['id'],))
        user_role_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
    
    # Handle error messages
    error_message = None
    if error == "password_mismatch":
        error_message = "Passwords do not match. Please try again."
    elif error == "username_taken":
        error_message = "Username already exists. Please choose a different username."
    elif error == "no_roles":
        error_message = "Please select at least one role."
    
    return templates.TemplateResponse(
        "person_details.html",
        {
            "request": request,
            "person": person,
            "addresses": addresses,
            "contacts": contacts,
            "roles": roles,
            "user_for_person": user_for_person,
            "all_roles": all_roles,
            "user_role_ids": user_role_ids,
            "error_message": error_message,
        }
    )

@router.get("/manage/person/{person_id}/add_user", response_class=HTMLResponse)
async def add_user_for_person_form(request: Request, person_id: int):
    # Only allow if not already a user
    user_for_person = UserService.get_user_by_person_id(person_id)
    if user_for_person:
        return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)
    roles = UserService.get_all_roles()
    return templates.TemplateResponse("add_user_for_person.html", {"request": request, "person_id": person_id, "roles": roles})

@router.post("/manage/person/{person_id}/add_user")
async def add_user_for_person(request: Request, person_id: int, username: str = Form(...), password: str = Form(...), roles: list = Form(...), active: bool = Form(True)):
    # Only allow if not already a user
    user_for_person = UserService.get_user_by_person_id(person_id)
    if user_for_person:
        return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)
    UserService.add_user(username, password, person_id, [int(r) for r in roles], active)
    return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)

@router.post("/manage/person/{person_id}/add_user_modal")
async def add_user_for_person_modal(request: Request, person_id: int, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...), active: str = Form("1"), roles: list = Form(...)):
    admin_required(request)
    
    # Check if person is already a user
    user_for_person = UserService.get_user_by_person_id(person_id)
    if user_for_person:
        return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)
    
    # Validate password confirmation
    if password != confirm_password:
        # Redirect back with error - we'll need to handle this differently
        return RedirectResponse(url=f"/manage/person/{person_id}?error=password_mismatch", status_code=303)
    
    # Check if username is unique
    if UserService.is_username_taken(username):
        return RedirectResponse(url=f"/manage/person/{person_id}?error=username_taken", status_code=303)
    
    # Validate that at least one role is selected
    if not roles:
        return RedirectResponse(url=f"/manage/person/{person_id}?error=no_roles", status_code=303)
    
    # Add the user
    active_bool = active == "1"
    UserService.add_user(username, password, person_id, [int(r) for r in roles], active_bool)
    
    return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)

@router.get("/manage/person/{person_id}/edit_user", response_class=HTMLResponse)
async def edit_user_for_person_form(request: Request, person_id: int):
    user_for_person = UserService.get_user_by_person_id(person_id)
    if not user_for_person:
        return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)
    all_roles = UserService.get_all_roles()
    # Get user roles
    conn = DBService.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT role_id FROM user_roles WHERE user_id = %s', (user_for_person['id'],))
    user_role_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return templates.TemplateResponse("edit_user_for_person.html", {"request": request, "person_id": person_id, "user": user_for_person, "all_roles": all_roles, "user_role_ids": user_role_ids})

@router.post("/manage/person/{person_id}/edit_user")
async def edit_user_for_person(request: Request, person_id: int, username: str = Form(...), password: str = Form(None), active: bool = Form(False), roles: list = Form(...)):
    user_for_person = UserService.get_user_by_person_id(person_id)
    if not user_for_person:
        return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)
    UserService.update_user(user_for_person['id'], username, password, person_id, [int(r) for r in roles], active)
    return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)

@router.post("/manage/person/{person_id}/delete_user")
async def delete_user_for_person(request: Request, person_id: int):
    user_for_person = UserService.get_user_by_person_id(person_id)
    if user_for_person:
        UserService.delete_user(user_for_person['id'])
    return RedirectResponse(url=f"/manage/person/{person_id}", status_code=303)