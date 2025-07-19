# Source Code

This document provides an organized overview of the source code for the Student Management System (SMS) application. Files are grouped by their type and purpose, with a brief description for each group and file. File paths are relative to the project root (`sms`).

---

## FastAPI Routers
Routers define the main API endpoints and web routes for the application. Each router typically corresponds to a major module or feature.

### app/pages/academic.py
**Description:** Handles all academic-related routes (sessions, courses, degrees, offerings, student/faculty dashboards, etc.).

```python
from fastapi import APIRouter, Request, Form, Query
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.services.academic_service import AcademicService
from app.services.user_service import UserService
from starlette.status import HTTP_303_SEE_OTHER

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def admin_required(request: Request):
    if request.session.get("role") != "Administrator":
        return RedirectResponse(url="/", status_code=303)

def faculty_required(request: Request):
    if request.session.get("role") not in ["Administrator", "Faculty"]:
        return RedirectResponse(url="/", status_code=303)

def student_required(request: Request):
    if request.session.get("role") not in ["Administrator", "Faculty", "Student"]:
        return RedirectResponse(url="/", status_code=303)

# Academic Sessions Management (Admin only)
@router.get("/academic/sessions", response_class=HTMLResponse)
async def list_sessions(request: Request):
    admin_required(request)
    sessions = AcademicService.get_all_sessions()
    return templates.TemplateResponse("academic/sessions_list.html", {"request": request, "sessions": sessions})

@router.get("/academic/sessions/add", response_class=HTMLResponse)
async def add_session_form(request: Request):
    admin_required(request)
    return templates.TemplateResponse("academic/session_add.html", {"request": request})

@router.post("/academic/sessions/add")
async def add_session(request: Request, name: str = Form(...), start_date: str = Form(...), end_date: str = Form(...), is_active: bool = Form(True)):
    admin_required(request)
    AcademicService.add_session(name, start_date, end_date, is_active)
    return RedirectResponse(url="/academic/sessions", status_code=303)

@router.get("/academic/sessions/{session_id}/edit", response_class=HTMLResponse)
async def edit_session_form(request: Request, session_id: int):
    admin_required(request)
    session = AcademicService.get_session(session_id)
    return templates.TemplateResponse("academic/session_edit.html", {"request": request, "session": session})

@router.post("/academic/sessions/{session_id}/edit")
async def edit_session(request: Request, session_id: int, name: str = Form(...), start_date: str = Form(...), end_date: str = Form(...), is_active: bool = Form(True)):
    admin_required(request)
    AcademicService.update_session(session_id, name, start_date, end_date, is_active)
    return RedirectResponse(url="/academic/sessions", status_code=303)

@router.post("/academic/sessions/{session_id}/delete")
async def delete_session(request: Request, session_id: int):
    admin_required(request)
    AcademicService.delete_session(session_id)
    return RedirectResponse(url="/academic/sessions", status_code=303)

# Courses Management (Admin only)
@router.get("/academic/courses", response_class=HTMLResponse)
async def list_courses(request: Request):
    admin_required(request)
    courses = AcademicService.get_all_courses()
    return templates.TemplateResponse("academic/courses_list.html", {"request": request, "courses": courses})

@router.get("/academic/courses/add", response_class=HTMLResponse)
async def add_course_form(request: Request):
    admin_required(request)
    return templates.TemplateResponse("academic/course_add.html", {"request": request})

@router.post("/academic/courses/add")
async def add_course(request: Request, code: str = Form(...), name: str = Form(...), description: str = Form(...), credits: int = Form(3)):
    admin_required(request)
    AcademicService.add_course(code, name, description, credits)
    return RedirectResponse(url="/academic/courses", status_code=303)

@router.get("/academic/courses/{course_id}/edit", response_class=HTMLResponse)
async def edit_course_form(request: Request, course_id: int):
    admin_required(request)
    course = AcademicService.get_course(course_id)
    return templates.TemplateResponse("academic/course_edit.html", {"request": request, "course": course})

@router.post("/academic/courses/{course_id}/edit")
async def edit_course(request: Request, course_id: int, code: str = Form(...), name: str = Form(...), description: str = Form(...), credits: int = Form(3), is_active: bool = Form(True)):
    admin_required(request)
    AcademicService.update_course(course_id, code, name, description, credits, is_active)
    return RedirectResponse(url="/academic/courses", status_code=303)

@router.post("/academic/courses/{course_id}/delete")
async def delete_course(request: Request, course_id: int):
    admin_required(request)
    AcademicService.delete_course(course_id)
    return RedirectResponse(url="/academic/courses", status_code=303)

# Course Offerings Management (Admin only)
@router.get("/academic/offerings", response_class=HTMLResponse)
async def list_offerings(request: Request, session_id: str = Query(None)):
    admin_required(request)
    
    # Convert session_id to int if it's not empty, otherwise use None
    session_id_int = None
    if session_id and session_id.strip():
        try:
            session_id_int = int(session_id)
        except ValueError:
            session_id_int = None
    
    offerings = AcademicService.get_course_offerings(session_id_int)
    sessions = AcademicService.get_active_sessions()
    return templates.TemplateResponse("academic/offerings_list.html", {
        "request": request, 
        "offerings": offerings, 
        "sessions": sessions,
        "selected_session": session_id_int
    })

@router.get("/academic/offerings/add", response_class=HTMLResponse)
async def add_offering_form(request: Request):
    admin_required(request)
    sessions = AcademicService.get_active_sessions()
    courses = AcademicService.get_active_courses()
    faculty = UserService.get_faculty_users()  # Get only faculty users
    return templates.TemplateResponse("academic/offering_add.html", {
        "request": request, 
        "sessions": sessions, 
        "courses": courses,
        "faculty": faculty
    })

@router.post("/academic/offerings/add")
async def add_offering(request: Request, session_id: int = Form(...), course_id: int = Form(...), faculty_id: int = Form(...), max_students: int = Form(50)):
    admin_required(request)
    AcademicService.add_course_offering(session_id, course_id, faculty_id, max_students)
    return RedirectResponse(url="/academic/offerings", status_code=303)

@router.get("/academic/offerings/{offering_id}/edit", response_class=HTMLResponse)
async def edit_offering_form(request: Request, offering_id: int):
    admin_required(request)
    offering = AcademicService.get_course_offerings()[0]  # Get specific offering
    sessions = AcademicService.get_active_sessions()
    courses = AcademicService.get_active_courses()
    faculty = UserService.get_faculty_users()  # Get only faculty users
    return templates.TemplateResponse("academic/offering_edit.html", {
        "request": request, 
        "offering": offering,
        "sessions": sessions, 
        "courses": courses,
        "faculty": faculty
    })

@router.post("/academic/offerings/{offering_id}/edit")
async def edit_offering(request: Request, offering_id: int, session_id: int = Form(...), course_id: int = Form(...), faculty_id: int = Form(...), max_students: int = Form(50), is_active: bool = Form(True)):
    admin_required(request)
    AcademicService.update_course_offering(offering_id, session_id, course_id, faculty_id, max_students, is_active)
    return RedirectResponse(url="/academic/offerings", status_code=303)

@router.post("/academic/offerings/{offering_id}/delete")
async def delete_offering(request: Request, offering_id: int):
    admin_required(request)
    AcademicService.delete_course_offering(offering_id)
    return RedirectResponse(url="/academic/offerings", status_code=303)

# Faculty Dashboard
@router.get("/faculty/dashboard", response_class=HTMLResponse)
async def faculty_dashboard(request: Request):
    faculty_required(request)
    faculty_id = request.session.get("user_id")
    offerings = AcademicService.get_faculty_offerings(faculty_id)
    return templates.TemplateResponse("academic/faculty_dashboard.html", {
        "request": request, 
        "offerings": offerings
    })

@router.get("/faculty/courses/{offering_id}", response_class=HTMLResponse)
async def faculty_course_details(request: Request, offering_id: int):
    faculty_required(request)
    faculty_id = request.session.get("user_id")
    offering = AcademicService.get_faculty_offerings(faculty_id)[0]  # Get specific offering
    students = AcademicService.get_course_students(offering_id)
    return templates.TemplateResponse("academic/faculty_course_details.html", {
        "request": request, 
        "offering": offering,
        "students": students
    })

@router.get("/faculty/students/{registration_id}/marks", response_class=HTMLResponse)
async def faculty_student_marks(request: Request, registration_id: int):
    faculty_required(request)
    # Get student marks for this registration
    marks = AcademicService.get_marks_by_registration(registration_id)
    # Get student and course information for this registration
    registration_info = AcademicService.get_registration_info(registration_id)
    return templates.TemplateResponse("academic/faculty_student_marks.html", {
        "request": request, 
        "marks": marks,
        "registration_id": registration_id,
        "registration_info": registration_info
    })

@router.post("/faculty/marks/add")
async def add_mark(request: Request, registration_id: int = Form(...), assignment_type: str = Form(...), marks_obtained: float = Form(...), total_marks: float = Form(100.0), remarks: str = Form(None)):
    faculty_required(request)
    AcademicService.add_mark(registration_id, assignment_type, marks_obtained, total_marks, remarks)
    return RedirectResponse(url=f"/faculty/students/{registration_id}/marks", status_code=303)

# Student Dashboard
@router.get("/student/dashboard", response_class=HTMLResponse)
async def student_dashboard(request: Request):
    student_required(request)
    student_id = request.session.get("user_id")
    registrations = AcademicService.get_student_registrations(student_id)
    degrees = AcademicService.get_student_degrees(student_id)
    return templates.TemplateResponse("academic/student_dashboard.html", {
        "request": request, 
        "registrations": registrations,
        "degrees": degrees
    })

@router.get("/student/courses", response_class=HTMLResponse)
async def student_courses(request: Request, session_id: str = Query(None)):
    student_required(request)
    student_id = request.session.get("user_id")
    
    # Convert session_id to int if it's not empty, otherwise use None
    session_id_int = None
    if session_id and session_id.strip():
        try:
            session_id_int = int(session_id)
        except ValueError:
            session_id_int = None
    
    registrations = AcademicService.get_student_registrations(student_id, session_id_int)
    sessions = AcademicService.get_active_sessions()
    return templates.TemplateResponse("academic/student_courses.html", {
        "request": request, 
        "registrations": registrations,
        "sessions": sessions,
        "selected_session": session_id_int
    })

@router.get("/student/registration", response_class=HTMLResponse)
async def student_registration_form(request: Request, session_id: str = Query(None)):
    student_required(request)
    student_id = request.session.get("user_id")
    
    # Convert session_id to int if it's not empty, otherwise use None
    session_id_int = None
    if session_id and session_id.strip():
        try:
            session_id_int = int(session_id)
        except ValueError:
            session_id_int = None
    
    available_courses = AcademicService.get_available_courses_for_registration(student_id, session_id_int)
    sessions = AcademicService.get_active_sessions()
    return templates.TemplateResponse("academic/student_registration.html", {
        "request": request, 
        "available_courses": available_courses,
        "sessions": sessions,
        "selected_session": session_id_int
    })

@router.post("/student/register")
async def register_for_course(request: Request, offering_id: int = Form(...)):
    student_required(request)
    student_id = request.session.get("user_id")
    success, message = AcademicService.register_student_for_course(student_id, offering_id)
    if success:
        return RedirectResponse(url="/student/courses", status_code=303)
    else:
        return templates.TemplateResponse("academic/student_registration.html", {
            "request": request,
            "error": message
        })

@router.post("/student/drop")
async def drop_course(request: Request, registration_id: int = Form(...)):
    student_required(request)
    AcademicService.drop_course_registration(registration_id)
    return RedirectResponse(url="/student/courses", status_code=303)

@router.get("/student/marks", response_class=HTMLResponse)
async def student_marks(request: Request, offering_id: int = Query(None)):
    student_required(request)
    student_id = request.session.get("user_id")
    marks = AcademicService.get_student_marks(student_id, offering_id)
    return templates.TemplateResponse("academic/student_marks.html", {
        "request": request, 
        "marks": marks
    })

# Degrees Management (Admin only)
@router.get("/academic/degrees", response_class=HTMLResponse)
async def list_degrees(request: Request):
    admin_required(request)
    degrees = AcademicService.get_all_degrees()
    return templates.TemplateResponse("academic/degrees_list.html", {"request": request, "degrees": degrees})

@router.get("/academic/degrees/add", response_class=HTMLResponse)
async def add_degree_form(request: Request):
    admin_required(request)
    return templates.TemplateResponse("academic/degree_add.html", {"request": request})

@router.post("/academic/degrees/add")
async def add_degree(request: Request, name: str = Form(...), abbreviation: str = Form(...), description: str = Form(...)):
    admin_required(request)
    AcademicService.add_degree(name, abbreviation, description)
    return RedirectResponse(url="/academic/degrees", status_code=303)

@router.get("/academic/degrees/{degree_id}/edit", response_class=HTMLResponse)
async def edit_degree_form(request: Request, degree_id: int):
    admin_required(request)
    degree = AcademicService.get_degree(degree_id)
    return templates.TemplateResponse("academic/degree_edit.html", {"request": request, "degree": degree})

@router.post("/academic/degrees/{degree_id}/edit")
async def edit_degree(request: Request, degree_id: int, name: str = Form(...), abbreviation: str = Form(...), description: str = Form(...), is_active: bool = Form(True)):
    admin_required(request)
    AcademicService.update_degree(degree_id, name, abbreviation, description, is_active)
    return RedirectResponse(url="/academic/degrees", status_code=303)

# Print Degree (Student and Admin)
@router.get("/academic/degree/print/{student_id}", response_class=HTMLResponse)
async def print_degree(request: Request, student_id: int):
    student_required(request)
    # Check if current user is the student or admin
    current_user_id = request.session.get("user_id")
    if request.session.get("role") != "Administrator" and current_user_id != student_id:
        return RedirectResponse(url="/", status_code=303)
    
    degrees = AcademicService.get_student_degrees(student_id)
    return templates.TemplateResponse("academic/degree_print.html", {
        "request": request, 
        "degrees": degrees,
        "student_id": student_id
    }) 
```

### app/pages/login.py
**Description:** Handles login, logout, and authentication routes.

```python
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
```

### app/pages/user.py
**Description:** Manages user account routes (add, edit, list users, etc.).

```python
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
```

### app/pages/favicon.py
**Description:** Handles favicon management routes.

```python
from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter()

@router.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)
```

### app/pages/home.py
**Description:** Main home page and user profile routes.

```python
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
```

---

## FastAPI Services
Service modules encapsulate business logic and database operations for each domain.

### app/services/academic_service.py
**Description:** Academic domain logic (sessions, courses, degrees, offerings, registration, etc.).

```python
from app.services.db_service import DBService

class AcademicService:
    @staticmethod
    def get_all_sessions():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM academic_sessions ORDER BY start_date DESC')
        sessions = cursor.fetchall()
        cursor.close()
        conn.close()
        return sessions

    @staticmethod
    def get_active_sessions():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM academic_sessions WHERE is_active = TRUE ORDER BY start_date DESC')
        sessions = cursor.fetchall()
        cursor.close()
        conn.close()
        return sessions

    @staticmethod
    def get_session(session_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM academic_sessions WHERE id = %s', (session_id,))
        session = cursor.fetchone()
        cursor.close()
        conn.close()
        return session

    @staticmethod
    def add_session(name, start_date, end_date, is_active=True):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO academic_sessions (name, start_date, end_date, is_active) VALUES (%s, %s, %s, %s)',
            (name, start_date, end_date, is_active)
        )
        session_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return session_id

    @staticmethod
    def update_session(session_id, name, start_date, end_date, is_active):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE academic_sessions SET name=%s, start_date=%s, end_date=%s, is_active=%s WHERE id=%s',
            (name, start_date, end_date, is_active, session_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_session(session_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM academic_sessions WHERE id = %s', (session_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all_courses():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM courses ORDER BY code')
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        return courses

    @staticmethod
    def get_active_courses():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM courses WHERE is_active = TRUE ORDER BY code')
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        return courses

    @staticmethod
    def get_course(course_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM courses WHERE id = %s', (course_id,))
        course = cursor.fetchone()
        cursor.close()
        conn.close()
        return course

    @staticmethod
    def add_course(code, name, description, credits=3):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO courses (code, name, description, credits) VALUES (%s, %s, %s, %s)',
            (code, name, description, credits)
        )
        course_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return course_id

    @staticmethod
    def update_course(course_id, code, name, description, credits, is_active):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE courses SET code=%s, name=%s, description=%s, credits=%s, is_active=%s WHERE id=%s',
            (code, name, description, credits, is_active, course_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_course(course_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM courses WHERE id = %s', (course_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_course_offerings(session_id=None):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        if session_id:
            cursor.execute('''
                SELECT co.*, c.code, c.name as course_name, c.credits, 
                       s.name as session_name, 
                       CONCAT(p.first_name, ' ', p.last_name) as faculty_name
                FROM course_offerings co
                JOIN courses c ON co.course_id = c.id
                JOIN academic_sessions s ON co.session_id = s.id
                JOIN users u ON co.faculty_id = u.id
                JOIN person p ON u.person_id = p.id
                WHERE co.session_id = %s AND co.is_active = TRUE
                ORDER BY c.code
            ''', (session_id,))
        else:
            cursor.execute('''
                SELECT co.*, c.code, c.name as course_name, c.credits, 
                       s.name as session_name, 
                       CONCAT(p.first_name, ' ', p.last_name) as faculty_name
                FROM course_offerings co
                JOIN courses c ON co.course_id = c.id
                JOIN academic_sessions s ON co.session_id = s.id
                JOIN users u ON co.faculty_id = u.id
                JOIN person p ON u.person_id = p.id
                WHERE co.is_active = TRUE
                ORDER BY s.start_date DESC, c.code
            ''')
        offerings = cursor.fetchall()
        cursor.close()
        conn.close()
        return offerings

    @staticmethod
    def get_faculty_offerings(faculty_id, session_id=None):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        if session_id:
            cursor.execute('''
                SELECT co.*, c.code, c.name as course_name, c.credits, 
                       s.name as session_name
                FROM course_offerings co
                JOIN courses c ON co.course_id = c.id
                JOIN academic_sessions s ON co.session_id = s.id
                WHERE co.faculty_id = %s AND co.session_id = %s AND co.is_active = TRUE
                ORDER BY c.code
            ''', (faculty_id, session_id))
        else:
            cursor.execute('''
                SELECT co.*, c.code, c.name as course_name, c.credits, 
                       s.name as session_name
                FROM course_offerings co
                JOIN courses c ON co.course_id = c.id
                JOIN academic_sessions s ON co.session_id = s.id
                WHERE co.faculty_id = %s AND co.is_active = TRUE
                ORDER BY s.start_date DESC, c.code
            ''', (faculty_id,))
        offerings = cursor.fetchall()
        cursor.close()
        conn.close()
        return offerings

    @staticmethod
    def add_course_offering(session_id, course_id, faculty_id, max_students=50):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO course_offerings (session_id, course_id, faculty_id, max_students) VALUES (%s, %s, %s, %s)',
            (session_id, course_id, faculty_id, max_students)
        )
        offering_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return offering_id

    @staticmethod
    def update_course_offering(offering_id, session_id, course_id, faculty_id, max_students, is_active):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE course_offerings SET session_id=%s, course_id=%s, faculty_id=%s, max_students=%s, is_active=%s WHERE id=%s',
            (session_id, course_id, faculty_id, max_students, is_active, offering_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_course_offering(offering_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM course_offerings WHERE id = %s', (offering_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_student_registrations(student_id, session_id=None):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        if session_id:
            cursor.execute('''
                SELECT sr.*, c.code, c.name as course_name, c.credits,
                       s.name as session_name, co.max_students,
                       CONCAT(p.first_name, ' ', p.last_name) as faculty_name
                FROM student_registrations sr
                JOIN course_offerings co ON sr.offering_id = co.id
                JOIN courses c ON co.course_id = c.id
                JOIN academic_sessions s ON co.session_id = s.id
                JOIN users u ON co.faculty_id = u.id
                JOIN person p ON u.person_id = p.id
                WHERE sr.student_id = %s AND co.session_id = %s
                ORDER BY c.code
            ''', (student_id, session_id))
        else:
            cursor.execute('''
                SELECT sr.*, c.code, c.name as course_name, c.credits,
                       s.name as session_name, co.max_students,
                       CONCAT(p.first_name, ' ', p.last_name) as faculty_name
                FROM student_registrations sr
                JOIN course_offerings co ON sr.offering_id = co.id
                JOIN courses c ON co.course_id = c.id
                JOIN academic_sessions s ON co.session_id = s.id
                JOIN users u ON co.faculty_id = u.id
                JOIN person p ON u.person_id = p.id
                WHERE sr.student_id = %s
                ORDER BY s.start_date DESC, c.code
            ''', (student_id,))
        registrations = cursor.fetchall()
        cursor.close()
        conn.close()
        return registrations

    @staticmethod
    def register_student_for_course(student_id, offering_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if already registered
        cursor.execute('SELECT id FROM student_registrations WHERE student_id = %s AND offering_id = %s', 
                      (student_id, offering_id))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Already registered for this course"
        
        # Check if course is full
        cursor.execute('SELECT current_students, max_students FROM course_offerings WHERE id = %s', (offering_id,))
        offering = cursor.fetchone()
        if offering and int(offering['current_students']) >= int(offering['max_students']):
            cursor.close()
            conn.close()
            return False, "Course is full"
        
        # Register student
        cursor.execute(
            'INSERT INTO student_registrations (student_id, offering_id, registration_date) VALUES (%s, %s, CURDATE())',
            (student_id, offering_id)
        )
        
        # Update current students count
        cursor.execute('UPDATE course_offerings SET current_students = current_students + 1 WHERE id = %s', (offering_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Registration successful"

    @staticmethod
    def drop_course_registration(registration_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get offering_id before deleting
        cursor.execute('SELECT offering_id FROM student_registrations WHERE id = %s', (registration_id,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return False
        
        offering_id = result['offering_id']
        
        # Delete registration
        cursor.execute('DELETE FROM student_registrations WHERE id = %s', (registration_id,))
        
        # Update current students count
        cursor.execute('UPDATE course_offerings SET current_students = current_students - 1 WHERE id = %s', (offering_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def get_course_students(offering_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT sr.*, CONCAT(p.first_name, ' ', p.last_name) as student_name,
                   u.username as student_username
            FROM student_registrations sr
            JOIN users u ON sr.student_id = u.id
            JOIN person p ON u.person_id = p.id
            WHERE sr.offering_id = %s
            ORDER BY p.last_name, p.first_name
        ''', (offering_id,))
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return students

    @staticmethod
    def get_student_marks(student_id, offering_id=None):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        if offering_id:
            cursor.execute('''
                SELECT m.*, c.code, c.name as course_name, sr.offering_id
                FROM marks m
                JOIN student_registrations sr ON m.registration_id = sr.id
                JOIN course_offerings co ON sr.offering_id = co.id
                JOIN courses c ON co.course_id = c.id
                WHERE sr.student_id = %s AND sr.offering_id = %s
                ORDER BY m.assignment_type, m.create_dt
            ''', (student_id, offering_id))
        else:
            cursor.execute('''
                SELECT m.*, c.code, c.name as course_name, sr.offering_id
                FROM marks m
                JOIN student_registrations sr ON m.registration_id = sr.id
                JOIN course_offerings co ON sr.offering_id = co.id
                JOIN courses c ON co.course_id = c.id
                WHERE sr.student_id = %s
                ORDER BY c.code, m.assignment_type, m.create_dt
            ''', (student_id,))
        marks = cursor.fetchall()
        cursor.close()
        conn.close()
        return marks

    @staticmethod
    def get_marks_by_registration(registration_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT m.*, c.code, c.name as course_name, sr.offering_id
            FROM marks m
            JOIN student_registrations sr ON m.registration_id = sr.id
            JOIN course_offerings co ON sr.offering_id = co.id
            JOIN courses c ON co.course_id = c.id
            WHERE m.registration_id = %s
            ORDER BY m.assignment_type, m.create_dt
        ''', (registration_id,))
        marks = cursor.fetchall()
        cursor.close()
        conn.close()
        return marks

    @staticmethod
    def get_registration_info(registration_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT sr.*, 
                   CONCAT(p.first_name, ' ', p.last_name) as student_name,
                   u.username as student_username,
                   c.code as course_code, 
                   c.name as course_name,
                   c.credits,
                   s.name as session_name
            FROM student_registrations sr
            JOIN users u ON sr.student_id = u.id
            JOIN person p ON u.person_id = p.id
            JOIN course_offerings co ON sr.offering_id = co.id
            JOIN courses c ON co.course_id = c.id
            JOIN academic_sessions s ON co.session_id = s.id
            WHERE sr.id = %s
        ''', (registration_id,))
        registration_info = cursor.fetchone()
        cursor.close()
        conn.close()
        return registration_info

    @staticmethod
    def add_mark(registration_id, assignment_type, marks_obtained, total_marks=100.00, remarks=None):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO marks (registration_id, assignment_type, marks_obtained, total_marks, remarks) VALUES (%s, %s, %s, %s, %s)',
            (registration_id, assignment_type, marks_obtained, total_marks, remarks)
        )
        mark_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return mark_id

    @staticmethod
    def update_mark(mark_id, assignment_type, marks_obtained, total_marks, remarks):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE marks SET assignment_type=%s, marks_obtained=%s, total_marks=%s, remarks=%s WHERE id=%s',
            (assignment_type, marks_obtained, total_marks, remarks, mark_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_mark(mark_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM marks WHERE id = %s', (mark_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all_degrees():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM degrees ORDER BY name')
        degrees = cursor.fetchall()
        cursor.close()
        conn.close()
        return degrees

    @staticmethod
    def get_student_degrees(student_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT sd.*, d.name as degree_name, d.abbreviation
            FROM student_degrees sd
            JOIN degrees d ON sd.degree_id = d.id
            WHERE sd.student_id = %s
            ORDER BY sd.enrollment_date DESC
        ''', (student_id,))
        degrees = cursor.fetchall()
        cursor.close()
        conn.close()
        return degrees

    @staticmethod
    def enroll_student_in_degree(student_id, degree_id, expected_completion_date):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO student_degrees (student_id, degree_id, enrollment_date, expected_completion_date) VALUES (%s, %s, CURDATE(), %s)',
            (student_id, degree_id, expected_completion_date)
        )
        enrollment_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return enrollment_id

    @staticmethod
    def get_available_courses_for_registration(student_id, session_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT co.*, c.code, c.name as course_name, c.credits, c.description,
                   CONCAT(p.first_name, ' ', p.last_name) as faculty_name
            FROM course_offerings co
            JOIN courses c ON co.course_id = c.id
            JOIN users u ON co.faculty_id = u.id
            JOIN person p ON u.person_id = p.id
            WHERE co.session_id = %s AND co.is_active = TRUE
            AND co.id NOT IN (
                SELECT offering_id FROM student_registrations 
                WHERE student_id = %s AND status = 'Registered'
            )
            AND co.current_students < co.max_students
            ORDER BY c.code
        ''', (session_id, student_id))
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        return courses 

    @staticmethod
    def get_degree(degree_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM degrees WHERE id = %s', (degree_id,))
        degree = cursor.fetchone()
        cursor.close()
        conn.close()
        return degree

    @staticmethod
    def update_degree(degree_id, name, abbreviation, description, is_active):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE degrees SET name=%s, abbreviation=%s, description=%s, is_active=%s WHERE id=%s',
            (name, abbreviation, description, is_active, degree_id)
        )
        conn.commit()
        cursor.close()
        conn.close() 

    @staticmethod
    def add_degree(name, abbreviation, description, is_active=True):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO degrees (name, abbreviation, description, is_active) VALUES (%s, %s, %s, %s)',
            (name, abbreviation, description, is_active)
        )
        conn.commit()
        cursor.close()
        conn.close() 
```

### app/services/user_service.py
**Description:** User account management logic.

```python
from app.services.db_service import DBService

class UserService:
    @staticmethod
    def list_users():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT users.id, users.username, users.active, person.first_name, person.last_name,
                   GROUP_CONCAT(roles.name) AS roles
            FROM users
            JOIN person ON users.person_id = person.id
            LEFT JOIN user_roles ON users.id = user_roles.user_id
            LEFT JOIN roles ON user_roles.role_id = roles.id
            GROUP BY users.id
        ''')
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users

    @staticmethod
    def get_user(user_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT users.*, person.first_name, person.last_name,
                   GROUP_CONCAT(roles.name) AS roles
            FROM users
            JOIN person ON users.person_id = person.id
            LEFT JOIN user_roles ON users.id = user_roles.user_id
            LEFT JOIN roles ON user_roles.role_id = roles.id
            WHERE users.id = %s
            GROUP BY users.id
        ''', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def add_user(username, password, person_id, role_ids, active=True):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password, person_id, active)
            VALUES (%s, %s, %s, %s)
        ''', (username, password, person_id, active))
        user_id = cursor.lastrowid
        for role_id in role_ids:
            cursor.execute('INSERT INTO user_roles (user_id, role_id) VALUES (%s, %s)', (user_id, role_id))
        conn.commit()
        cursor.close()
        conn.close()
        return user_id

    @staticmethod
    def update_user(user_id, username, password, person_id, role_ids, active):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        if password:
            cursor.execute('''
                UPDATE users SET username=%s, password=%s, person_id=%s, active=%s WHERE id=%s
            ''', (username, password, person_id, active, user_id))
        else:
            cursor.execute('''
                UPDATE users SET username=%s, person_id=%s, active=%s WHERE id=%s
            ''', (username, person_id, active, user_id))
        cursor.execute('DELETE FROM user_roles WHERE user_id=%s', (user_id,))
        for role_id in role_ids:
            cursor.execute('INSERT INTO user_roles (user_id, role_id) VALUES (%s, %s)', (user_id, role_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_user(user_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM user_roles WHERE user_id=%s', (user_id,))
        cursor.execute('DELETE FROM users WHERE id=%s', (user_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def toggle_active(user_id, active):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET active=%s WHERE id=%s', (active, user_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all_roles():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, name FROM roles')
        roles = cursor.fetchall()
        cursor.close()
        conn.close()
        return roles

    @staticmethod
    def get_all_people():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, first_name, last_name FROM person')
        people = cursor.fetchall()
        cursor.close()
        conn.close()
        return people

    @staticmethod
    def get_faculty_users():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT users.id, users.username, person.first_name, person.last_name
            FROM users
            JOIN person ON users.person_id = person.id
            JOIN user_roles ON users.id = user_roles.user_id
            JOIN roles ON user_roles.role_id = roles.id
            WHERE roles.name = 'Faculty' AND users.active = TRUE
            ORDER BY person.first_name, person.last_name
        ''')
        faculty = cursor.fetchall()
        cursor.close()
        conn.close()
        return faculty

    @staticmethod
    def search_users(username="", role="", active=""):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT users.id, users.username, users.active, users.person_id, person.first_name, person.last_name,
                   GROUP_CONCAT(roles.name) AS roles
            FROM users
            JOIN person ON users.person_id = person.id
            LEFT JOIN user_roles ON users.id = user_roles.user_id
            LEFT JOIN roles ON user_roles.role_id = roles.id
            WHERE 1=1
        '''
        params = []
        if username:
            query += " AND users.username LIKE %s"
            params.append(f"%{username}%")
        if role:
            query += " AND roles.name = %s"
            params.append(role)
        if active != "":
            query += " AND users.active = %s"
            params.append(bool(int(active)))
        query += " GROUP BY users.id"
        cursor.execute(query, params)
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users 

    @staticmethod
    def get_user_by_person_id(person_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE person_id = %s', (person_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def is_username_taken(username):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = %s', (username,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count > 0 

    @staticmethod
    def update_user_password(user_id, new_password):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET password = %s WHERE id = %s', (new_password, user_id))
        conn.commit()
        cursor.close()
        conn.close() 
```

### app/services/auth_service.py
**Description:** Authentication and password management logic.

```python
import os
from app.services.db_service import DBService

class AuthService:
    @staticmethod
    def login(username, password, role):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT users.id, users.username, roles.name AS role,
                   person.first_name, person.last_name
            FROM users
            JOIN user_roles ON users.id = user_roles.user_id
            JOIN roles ON roles.id = user_roles.role_id
            JOIN person ON users.person_id = person.id
            WHERE users.username=%s AND users.password=%s AND roles.name=%s AND users.active=TRUE
        ''', (username, password, role))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
```

### app/services/person_service.py
**Description:** Person domain logic (students, faculty, personal info, etc.).

```python
from app.services.db_service import DBService

class PersonService:
    @staticmethod
    def get_person(person_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM person WHERE id=%s", (person_id,))
        person = cursor.fetchone()
        cursor.close()
        conn.close()
        return person

    @staticmethod
    def get_addresses(person_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM addresses WHERE person_id=%s", (person_id,))
        addresses = cursor.fetchall()
        cursor.close()
        conn.close()
        return addresses

    @staticmethod
    def get_contacts(person_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM contact_info WHERE person_id=%s",
            (person_id,)
        )
        contacts = cursor.fetchall()
        cursor.close()
        conn.close()
        return contacts

    @staticmethod
    def get_roles(person_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT roles.name FROM users
            JOIN user_roles ON users.id = user_roles.user_id
            JOIN roles ON user_roles.role_id = roles.id
            WHERE users.person_id=%s
        """, (person_id,))
        roles = [row["name"] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return roles

    @staticmethod
    def update_person(person_id, first_name, last_name, birth_date, gender):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE person SET first_name=%s, last_name=%s, birth_date=%s, gender=%s WHERE id=%s",
            (first_name, last_name, birth_date, gender, person_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_person(person_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM person WHERE id=%s", (person_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def list_persons():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM person")
        persons = cursor.fetchall()
        cursor.close()
        conn.close()
        return persons

    @staticmethod
    def add_person(first_name, last_name, birth_date, gender):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO person (first_name, last_name, birth_date, gender) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, birth_date, gender),
        )
        person_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return person_id

    @staticmethod
    def add_address(person_id, address_type, address_line1, address_line2, city, state, postal_code, country):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO addresses (person_id, address_type, address_line1, address_line2, city, state, postal_code, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (person_id, address_type, address_line1, address_line2, city, state, postal_code, country),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def add_contact(person_id, contact_type, contact_value):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contact_info (person_id, contact_type, contact_value) VALUES (%s, %s, %s)",
            (person_id, contact_type, contact_value),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_address(address_id, address_type, address_line1, address_line2, city, state, postal_code, country):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE addresses SET address_type=%s, address_line1=%s, address_line2=%s, city=%s, state=%s, postal_code=%s, country=%s WHERE id=%s",
            (address_type, address_line1, address_line2, city, state, postal_code, country, address_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_address(address_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM addresses WHERE id=%s", (address_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_contact(contact_id, contact_type, contact_value):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE contact_info SET contact_type=%s, contact_value=%s WHERE id=%s",
            (contact_type, contact_value, contact_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_contact(contact_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contact_info WHERE id=%s", (contact_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def count_persons(first_name, last_name, birth_date, gender, role):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT COUNT(*)
            FROM person
            LEFT JOIN users ON users.person_id = person.id
            LEFT JOIN user_roles ON users.id = user_roles.user_id
            LEFT JOIN roles ON user_roles.role_id = roles.id
            WHERE 1=1
        """
        params = []
        if first_name:
            query += " AND person.first_name LIKE %s"
            params.append(f"%{first_name}%")
        if last_name:
            query += " AND person.last_name LIKE %s"
            params.append(f"%{last_name}%")
        if birth_date:
            query += " AND person.birth_date = %s"
            params.append(birth_date)
        if gender:
            query += " AND person.gender = %s"
            params.append(gender)
        if role:
            query += " AND roles.name = %s"
            params.append(role)
        cursor.execute(query, params)
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count

    @staticmethod
    def search_persons(first_name, last_name, birth_date, gender, role, offset, limit, sort_by="first_name", sort_order="asc"):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        # Whitelist allowed columns to prevent SQL injection
        allowed_sort_columns = {
            "id": "person.id",
            "first_name": "person.first_name",
            "last_name": "person.last_name",
            "birth_date": "person.birth_date",
            "gender": "person.gender",
            "role": "roles.name"
        }
        sort_column = allowed_sort_columns.get(sort_by, "person.first_name")
        sort_order = "desc" if sort_order == "desc" else "asc"
        query = f"""
            SELECT person.id, person.first_name, person.last_name, person.birth_date, person.gender, roles.name as role
            FROM person
            LEFT JOIN users ON users.person_id = person.id
            LEFT JOIN user_roles ON users.id = user_roles.user_id
            LEFT JOIN roles ON user_roles.role_id = roles.id
            WHERE 1=1
        """
        params = []
        if first_name:
            query += " AND person.first_name LIKE %s"
            params.append(f"%{first_name}%")
        if last_name:
            query += " AND person.last_name LIKE %s"
            params.append(f"%{last_name}%")
        if birth_date:
            query += " AND person.birth_date = %s"
            params.append(birth_date)
        if gender:
            query += " AND person.gender = %s"
            params.append(gender)
        if role:
            query += " AND roles.name = %s"
            params.append(role)
        query += f" ORDER BY {sort_column} {sort_order} LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        cursor.execute(query, params)
        persons = cursor.fetchall()
        cursor.close()
        conn.close()
        return persons 
```

### app/services/db_service.py
**Description:** Low-level database access and utility functions.

```python
import mysql.connector
import os

class DBService:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
```

---

## Middleware
Middleware modules provide cross-cutting functionality such as authentication and cache control.

### app/middleware/core.py
**Description:** Implements session authentication and disables browser caching for sensitive pages.

```python
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import RedirectResponse

class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

class AuthRequiredMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        allowed_paths = ["/", "/login", "/logout", "/favicon.ico", "/profile", "/change_password", "/student", "/faculty", "/academic"]
        if (
            request.url.path not in allowed_paths
            and not request.url.path.startswith("/static")
            and not request.session.get("user_id")
        ):
            return RedirectResponse(url="/")
        return await call_next(request)
```

---

## Jinja2 Templates
Templates define the HTML structure for all web pages. They are rendered by FastAPI endpoints and use Jinja2 syntax for dynamic content.

### app/templates/academic/faculty_student_marks.html
**Description:** Faculty view and add marks for a student in a course.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Student Marks - Faculty</title>
    <link rel="stylesheet" href="{{ request.url_for('static', path='style.css') }}">
    <style>
        .dashboard-container {
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }
        
        .section {
            background: #fff;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #e9ecef;
        }
        
        .section h2 {
            color: #495057;
            margin-bottom: 20px;
            font-size: 1.5em;
            font-weight: 600;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 10px;
        }
        
        .marks-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .marks-table th,
        .marks-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }
        
        .marks-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #495057;
        }
        
        .add-mark-form {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            border: 1px solid #e9ecef;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .empty-message {
            text-align: center;
            color: #6c757d;
            font-style: italic;
            padding: 40px;
        }
    </style>
</head>
<body>
    {% include "header.html" %}
    <main>
        <div class="dashboard-container">
            <div class="section">
                <h2>Student Marks</h2>
                
                {% if registration_info %}
                <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 20px; border: 1px solid #e9ecef;">
                    <h3 style="margin-top: 0; color: #495057;">Course & Student Information</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
                        <div>
                            <strong>Course:</strong> {{ registration_info.course_code }} - {{ registration_info.course_name }}
                        </div>
                        <div>
                            <strong>Student:</strong> {{ registration_info.student_name }} ({{ registration_info.student_username }})
                        </div>
                        <div>
                            <strong>Session:</strong> {{ registration_info.session_name }}
                        </div>
                        <div>
                            <strong>Credits:</strong> {{ registration_info.credits }}
                        </div>
                    </div>
                </div>
                {% endif %}
                
                {% if marks %}
                    <table class="marks-table">
                        <thead>
                            <tr>
                                <th>Assignment Type</th>
                                <th>Marks Obtained</th>
                                <th>Total Marks</th>
                                <th>Percentage</th>
                                <th>Remarks</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                        {% for mark in marks %}
                            <tr>
                                <td>{{ mark.assignment_type }}</td>
                                <td>{{ mark.marks_obtained }}</td>
                                <td>{{ mark.total_marks }}</td>
                                <td>{{ "%.1f"|format((mark.marks_obtained / mark.total_marks) * 100) }}%</td>
                                <td>{{ mark.remarks or '' }}</td>
                                <td>{{ mark.create_dt }}</td>
                            </tr>
                        {% endfor %}
                        </tbody>
                    </table>
                {% else %}
                    <div class="empty-message">
                        <p>No marks recorded for this student yet.</p>
                    </div>
                {% endif %}
                
                <div class="add-mark-form">
                    <h3>Add New Mark</h3>
                    <form method="POST" action="/faculty/marks/add">
                        <input type="hidden" name="registration_id" value="{{ registration_id }}">
                        
                        <div class="form-row">
                            <div>
                                <label for="assignment_type">Assignment Type:</label>
                                <select id="assignment_type" name="assignment_type" required>
                                    <option value="">Select Assignment Type</option>
                                    <option value="Midterm">Midterm</option>
                                    <option value="Final">Final</option>
                                    <option value="Assignment">Assignment</option>
                                    <option value="Project">Project</option>
                                    <option value="Participation">Participation</option>
                                </select>
                            </div>
                            <div>
                                <label for="marks_obtained">Marks Obtained:</label>
                                <input type="number" id="marks_obtained" name="marks_obtained" step="0.01" required>
                            </div>
                            <div>
                                <label for="total_marks">Total Marks:</label>
                                <input type="number" id="total_marks" name="total_marks" value="100" step="0.01" required>
                            </div>
                        </div>
                        
                        <div>
                            <label for="remarks">Remarks:</label>
                            <textarea id="remarks" name="remarks" rows="3"></textarea>
                        </div>
                        
                        <button type="submit" style="margin-top: 15px;">Add Mark</button>
                    </form>
                </div>
            </div>
        </div>
    </main>
    {% include "footer.html" %}
</body>
</html> 
```

### app/templates/academic/faculty_dashboard.html
**Description:** Faculty dashboard showing course offerings.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Faculty Dashboard</title>
    <link rel="stylesheet" href="{{ request.url_for('static', path='style.css') }}">
    <style>
        .dashboard-container {
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }
        
        .section {
            background: #fff;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #e9ecef;
        }
        
        .section h2 {
            color: #495057;
            margin-bottom: 20px;
            font-size: 1.5em;
            font-weight: 600;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 10px;
        }
        
        .course-grid {
            display: grid;
            gap: 20px;
        }
        
        .course-card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            border: 1px solid #e9ecef;
        }
        
        .course-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .course-code {
            font-weight: 600;
            color: #495057;
            font-size: 1.1em;
        }
        
        .course-details {
            color: #6c757d;
            font-size: 0.9em;
            line-height: 1.5;
        }
        
        .empty-message {
            text-align: center;
            color: #6c757d;
            font-style: italic;
            padding: 40px;
        }
    </style>
</head>
<body>
    {% include "header.html" %}
    <main>
        <div class="dashboard-container">
            <div class="section">
                <h2>My Course Offerings</h2>
                {% if offerings %}
                    <div class="course-grid">
                        {% for offering in offerings %}
                            <div class="course-card">
                                <div class="course-header">
                                    <span class="course-code">{{ offering.course_code }} - {{ offering.course_name }}</span>
                                </div>
                                <div class="course-details">
                                    <p><strong>Session:</strong> {{ offering.session_name }}</p>
                                    <p><strong>Students:</strong> {{ offering.current_students }}/{{ offering.max_students }}</p>
                                    <p><strong>Credits:</strong> {{ offering.credits }}</p>
                                </div>
                                <div style="margin-top: 15px; text-align: right;">
                                    <a href="/faculty/courses/{{ offering.id }}" class="btn-action" 
                                       style="background-color: #007bff; color: white; text-decoration: none; padding: 8px 16px; border-radius: 4px; display: inline-block;">
                                        Manage Students & Marks
                                    </a>
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                {% else %}
                    <div class="empty-message">
                        <p>You have no course offerings assigned.</p>
                    </div>
                {% endif %}
            </div>
        </div>
    </main>
    {% include "footer.html" %}
</body>
</html> 
```

### app/templates/academic/student_courses.html
**Description:** Student view of enrolled courses with drop functionality.

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Courses</title>
    <link rel="stylesheet" href="{{ request.url_for('static', path='style.css') }}">
    <style>
        .dashboard-container {
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }
        
        .section {
            background: #fff;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #e9ecef;
        }
        
        .section h2 {
            color: #495057;
            margin-bottom: 20px;
            font-size: 1.5em;
            font-weight: 600;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 10px;
        }
        
        .course-grid {
            display: grid;
            gap: 20px;
        }
        
        .course-card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            border: 1px solid #e9ecef;
        }
        
        .course-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .course-code {
            font-weight: 600;
            color: #495057;
            font-size: 1.1em;
        }
        
        .course-status {
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: 600;
        }
        
        .status-registered {
            background: #d4edda;
            color: #155724;
        }
        
        .status-completed {
            background: #cce5ff;
            color: #004085;
        }
        
        .status-dropped {
            background: #f8d7da;
            color: #721c24;
        }
        
        .course-details {
            color: #6c757d;
            font-size: 0.9em;
            line-height: 1.5;
        }
        
        .empty-message {
            text-align: center;
            color: #6c757d;
            font-style: italic;
            padding: 40px;
        }
    </style>
</head>
<body>
    {% include "header.html" %}
    <main>
        <div class="dashboard-container">
            <div class="section">
                <h2>My Enrolled Courses</h2>
                
                <!-- Session Filter -->
                <div style="margin-bottom: 20px;">
                    <form method="GET" action="/student/courses">
                        <label for="session_id">Filter by Session:</label>
                        <select name="session_id" id="session_id" onchange="this.form.submit()">
                            <option value="">All Sessions</option>
                            {% for session in sessions %}
                                <option value="{{ session.id }}" {% if selected_session == session.id %}selected{% endif %}>
                                    {{ session.name }}
                                </option>
                            {% endfor %}
                        </select>
                    </form>
                </div>
                
                {% if registrations %}
                    <div class="course-grid">
                        {% for registration in registrations %}
                            <div class="course-card">
                                <div class="course-header">
                                    <span class="course-code">{{ registration.course_code }} - {{ registration.course_name }}</span>
                                    <span class="course-status status-{{ registration.status.lower() }}">
                                        {{ registration.status }}
                                    </span>
                                </div>
                                <div class="course-details">
                                    <p><strong>Session:</strong> {{ registration.session_name }}</p>
                                    <p><strong>Faculty:</strong> {{ registration.faculty_name }}</p>
                                    <p><strong>Credits:</strong> {{ registration.credits }}</p>
                                    <p><strong>Registration Date:</strong> {{ registration.registration_date }}</p>
                                </div>
                                {% if registration.status.lower() == 'registered' %}
                                <div style="margin-top: 15px; text-align: right;">
                                    <form method="POST" action="/student/drop" style="display: inline;">
                                        <input type="hidden" name="registration_id" value="{{ registration.id }}">
                                        <button type="submit" class="btn-action" 
                                                onclick="return confirm('Are you sure you want to drop this course? This action cannot be undone.')"
                                                style="background-color: #dc3545; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">
                                            Drop Course
                                        </button>
                                    </form>
                                </div>
                                {% endif %}
                            </div>
                        {% endfor %}
                    </div>
                {% else %}
                    <div class="empty-message">
                        <p>You are not enrolled in any courses for this session.</p>
                        <p><a href="/student/registration">Register for courses</a></p>
                    </div>
                {% endif %}
            </div>
        </div>
    </main>
    {% include "footer.html" %}
</body>
</html> 
```

### app/templates/academic/offering_edit.html
**Description:** Edit a course offering (admin/faculty).

```html
<!DOCTYPE html>
<html>
<head>
    <title>Edit Course Offering</title>
    <link rel="stylesheet" href="{{ request.url_for('static', path='style.css') }}">
</head>
<body>
    {% include "header.html" %}
    <main>
        <div class="container">
            <h2>Edit Course Offering</h2>
            <form method="POST" action="/academic/offerings/{{ offering.id }}/edit">
                <div class="form-row">
                    <div>
                        <label for="session_id">Academic Session:</label>
                        <select id="session_id" name="session_id" required>
                            <option value="">Select Session</option>
                            {% for session in sessions %}
                                <option value="{{ session.id }}" {% if offering.session_id == session.id %}selected{% endif %}>{{ session.name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div>
                        <label for="course_id">Course:</label>
                        <select id="course_id" name="course_id" required>
                            <option value="">Select Course</option>
                            {% for course in courses %}
                                <option value="{{ course.id }}" {% if offering.course_id == course.id %}selected{% endif %}>{{ course.code }} - {{ course.name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>
                <div class="form-row">
                    <div>
                        <label for="faculty_id">Faculty:</label>
                        <select id="faculty_id" name="faculty_id" required>
                            <option value="">Select Faculty</option>
                            {% for faculty_member in faculty %}
                                <option value="{{ faculty_member.id }}" {% if offering.faculty_id == faculty_member.id %}selected{% endif %}>{{ faculty_member.first_name }} {{ faculty_member.last_name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div>
                        <label for="max_students">Maximum Students:</label>
                        <input type="number" id="max_students" name="max_students" value="{{ offering.max_students }}" min="1" max="200">
                    </div>
                </div>
                <div class="form-row">
                    <div style="display: flex; align-items: center; gap: 8px; margin-top: 30px;">
                        <input type="checkbox" id="is_active" name="is_active" {% if offering.is_active %}checked{% endif %}>
                        <label for="is_active" style="margin: 0;">Active</label>
                    </div>
                </div>
                <div style="display: flex; gap: 15px; margin-top: 24px;">
                    <button type="submit" class="btn">Update Offering</button>
                    <button type="button" class="btn btn-secondary" onclick="window.location.href='/academic/offerings'">Cancel</button>
                </div>
            </form>
        </div>
    </main>
    {% include "footer.html" %}
</body>
</html> 
```

### app/templates/academic/offering_add.html
**Description:** Add a new course offering (admin/faculty).

```html
<!DOCTYPE html>
<html>
<head>
    <title>Add Course Offering</title>
    <link rel="stylesheet" href="{{ request.url_for('static', path='style.css') }}">
</head>
<body>
    {% include "header.html" %}
    <main>
        <div class="container">
            <h2>Add Course Offering</h2>
            <form method="POST" action="/academic/offerings/add">
                <label for="session_id">Academic Session:</label>
                <select id="session_id" name="session_id" required>
                    <option value="">Select Session</option>
                    {% for session in sessions %}
                        <option value="{{ session.id }}">{{ session.name }}</option>
                    {% endfor %}
                </select>
                
                <label for="course_id">Course:</label>
                <select id="course_id" name="course_id" required>
                    <option value="">Select Course</option>
                    {% for course in courses %}
                        <option value="{{ course.id }}">{{ course.code }} - {{ course.name }}</option>
                    {% endfor %}
                </select>
                
                <label for="faculty_id">Faculty:</label>
                <select id="faculty_id" name="faculty_id" required>
                    <option value="">Select Faculty</option>
                    {% for faculty_member in faculty %}
                        <option value="{{ faculty_member.id }}">{{ faculty_member.first_name }} {{ faculty_member.last_name }}</option>
                    {% endfor %}
                </select>
                
                <label for="max_students">Maximum Students:</label>
                <input type="number" id="max_students" name="max_students" value="50" min="1" max="200">
                
                <button type="submit">Add Offering</button>
            </form>
        </div>
    </main>
    {% include "footer.html" %}
</body>
</html> 
```

### app/templates/academic/session_add.html
**Description:** Add a new academic session.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Add Academic Session</title>
    <link rel="stylesheet" href="{{ request.url_for('static', path='style.css') }}">
</head>
<body>
    {% include "header.html" %}
    <main>
        <div class="container">
            <h2>Add Academic Session</h2>
            <form method="POST" action="/academic/sessions/add">
                <div>
                    <label for="name">Session Name:</label>
                    <input type="text" id="name" name="name" required>
                </div>
                
                <div>
                    <label for="start_date">Start Date:</label>
                    <input type="date" id="start_date" name="start_date" required>
                </div>
                
                <div>
                    <label for="end_date">End Date:</label>
                    <input type="date" id="end_date" name="end_date" required>
                </div>
                
                <div>
                    <label for="is_active">Active:</label>
                    <input type="checkbox" id="is_active" name="is_active" checked>
                </div>
                
                <button type="submit">Add Session</button>
            </form>
        </div>
    </main>
    {% include "footer.html" %}
</body>
</html> 
```

### app/templates/academic/degree_edit.html
**Description:** Edit a degree program.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Edit Degree Program</title>
    <link rel="stylesheet" href="{{ request.url_for('static', path='style.css') }}">
</head>
<body>
    {% include "header.html" %}
    <main>
        <div class="container">
            <h2>Edit Degree Program</h2>
            <form method="POST" action="/academic/degrees/{{ degree.id }}/edit">
                <div class="form-row">
                    <div>
                        <label for="name">Degree Name:</label>
                        <input type="text" id="name" name="name" value="{{ degree.name }}" required>
                    </div>
                    <div>
                        <label for="abbreviation">Abbreviation:</label>
                        <input type="text" id="abbreviation" name="abbreviation" value="{{ degree.abbreviation }}" required>
                    </div>
                </div>
                <div class="form-row">
                    <div style="grid-column: 1 / span 2;">
                        <label for="description">Description:</label>
                        <textarea id="description" name="description" rows="4" style="width: 100%;">{{ degree.description }}</textarea>
                    </div>
                </div>
                <div class="form-row">
                    <div style="display: flex; align-items: center; gap: 8px; margin-top: 30px;">
                        <input type="checkbox" id="is_active" name="is_active" {% if degree.is_active %}checked{% endif %}>
                        <label for="is_active" style="margin: 0;">Active</label>
                    </div>
                </div>
                <div style="display: flex; gap: 15px; margin-top: 24px;">
                    <button type="submit" class="btn">Update Degree</button>
                    <button type="button" class="btn btn-secondary" onclick="window.location.href='/academic/degrees'">Cancel</button>
                </div>
            </form>
        </div>
    </main>
    {% include "footer.html" %}
</body>
</html> 
```

### app/templates/academic/course_edit.html
**Description:** Edit a course.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Edit Course</title>
    <link rel="stylesheet" href="{{ request.url_for('static', path='style.css') }}">
</head>
<body>
    {% include "header.html" %}
    <main>
        <div class="container">
            <h2>Edit Course</h2>
            <form method="POST" action="/academic/courses/{{ course.id }}/edit">
                <div class="form-row">
                    <div>
                        <label for="code">Course Code:</label>
                        <input type="text" id="code" name="code" value="{{ course.code }}" required>
                    </div>
                    <div>
                        <label for="name">Course Name:</label>
                        <input type="text" id="name" name="name" value="{{ course.name }}" required>
                    </div>
                </div>
                <div class="form-row">
                    <div style="grid-column: 1 / span 2;">
                        <label for="description">Description:</label>
                        <textarea id="description" name="description" rows="4" style="width: 100%;">{{ course.description }}</textarea>
                    </div>
                </div>
                <div class="form-row">
                    <div>
                        <label for="credits">Credits:</label>
                        <input type="number" id="credits" name="credits" value="{{ course.credits }}" min="1" max="10">
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; margin-top: 30px;">
                        <input type="checkbox" id="is_active" name="is_active" {% if course.is_active %}checked{% endif %}>
                        <label for="is_active" style="margin: 0;">Active</label>
                    </div>
                </div>
                <div style="display: flex; gap: 15px; margin-top: 24px;">
                    <button type="submit" class="btn">Update Course</button>
                    <button type="button" class="btn btn-secondary" onclick="window.location.href='/academic/courses'">Cancel</button>
                </div>
            </form>
        </div>
    </main>
    {% include "footer.html" %}
</body>
</html> 
```

### app/templates/academic/session_edit.html
**Description:** Edit an academic session.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Edit Academic Session</title>
    <link rel="stylesheet" href="{{ request.url_for('static', path='style.css') }}">
</head>
<body>
    {% include "header.html" %}
    <main>
        <div class="container">
            <h2>Edit Academic Session</h2>
            <form method="POST" action="/academic/sessions/{{ session.id }}/edit">
                <label for="name">Session Name:</label>
                <input type="text" id="name" name="name" value="{{ session.name }}" required style="margin-bottom: 16px;">
                <div class="form-row">
                    <div>
                        <label for="start_date">Start Date:</label>
                        <input type="date" id="start_date" name="start_date" value="{{ session.start_date }}" required>
                    </div>
                    <div>
                        <label for="end_date">End Date:</label>
                        <input type="date" id="end_date" name="end_date" value="{{ session.end_date }}" required>
                    </div>
                </div>
                <div style="margin: 16px 0 0 0;">
                    <label for="is_active" style="display: flex; align-items: center; gap: 8px;">
                        <input type="checkbox" id="is_active" name="is_active" {% if session.is_active %}checked{% endif %}>
                        <span>Active</span>
                    </label>
                </div>
                <div style="display: flex; gap: 15px; margin-top: 24px;">
                    <button type="submit" class="btn">Update Session</button>
                    <button type="button" class="btn btn-secondary" onclick="window.location.href='/academic/sessions'">Cancel</button>
                </div>
            </form>
        </div>
    </main>
    {% include "footer.html" %}
</body>
</html> 
```

### app/templates/academic/degree_print.html
**Description:** Print a student's degree certificate.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Degree Certificate</title>
    <link rel="stylesheet" href="{{ request.url_for('static', path='style.css') }}">
    <style>
        .print-container {
            max-width: 800px;
            margin: 40px auto;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            overflow: hidden;
            border: 1px solid #e9ecef;
        }
        
        .certificate-header {
            background: #f8f9fa;
            color: #495057;
            padding: 30px;
            text-align: center;
            border-bottom: 1px solid #e9ecef;
        }
        
        .certificate-header h1 {
            margin: 0;
            font-size: 2em;
            font-weight: 600;
            color: #343a40;
        }
        
        .certificate-content {
            padding: 40px;
        }
        
        .degree-info {
            background: #e8f5e8;
            border-left: 4px solid #4caf50;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
        }
        
        .degree-name {
            font-weight: 600;
            color: #2e7d32;
            font-size: 1.3em;
            margin-bottom: 10px;
        }
        
        .degree-details {
            color: #6c757d;
            font-size: 0.9em;
            line-height: 1.6;
        }
        
        .print-button {
            background: #007bff;
            color: #fff;
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 1em;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.2s;
            margin-top: 20px;
        }
        
        .print-button:hover {
            background: #0056b3;
        }
        
        .empty-message {
            text-align: center;
            color: #6c757d;
            font-style: italic;
            padding: 40px;
        }
        
        @media print {
            .print-button {
                display: none;
            }
            
            .print-container {
                box-shadow: none;
                border: none;
            }
        }
    </style>
</head>
<body>
    {% include "header.html" %}
    <main>
        <div class="print-container">
            <div class="certificate-header">
                <h1>Degree Certificate</h1>
            </div>
            
            <div class="certificate-content">
                {% if degrees %}
                    {% for degree in degrees %}
                        <div class="degree-info">
                            <div class="degree-name">{{ degree.degree_name }} ({{ degree.abbreviation }})</div>
                            <div class="degree-details">
                                <p><strong>Status:</strong> {{ degree.status }}</p>
                                <p><strong>Enrollment Date:</strong> {{ degree.enrollment_date }}</p>
                                {% if degree.expected_completion_date %}
                                    <p><strong>Expected Completion:</strong> {{ degree.expected_completion_date }}</p>
                                {% endif %}
                                {% if degree.actual_completion_date %}
                                    <p><strong>Completed:</strong> {{ degree.actual_completion_date }}</p>
                                {% endif %}
                                {% if degree.gpa %}
                                    <p><strong>GPA:</strong> {{ degree.gpa }}</p>
                                {% endif %}
                                {% if degree.credits_earned %}
                                    <p><strong>Credits Earned:</strong> {{ degree.credits_earned }}</p>
                                {% endif %}
                            </div>
                        </div>
                    {% endfor %}
                    
                    <button onclick="window.print()" class="print-button">Print Certificate</button>
                {% else %}
                    <div class="empty-message">
                        <p>No degree certificates available for printing.</p>
                        <p>Please contact your academic advisor if you believe this is an error.</p>
                    </div>
                {% endif %}
            </div>
        </div>
    </main>
    {% include "footer.html" %}
</body>
</html> 
```

---

## Static Files
Static files include CSS, JavaScript, and images used by the web application.

### app/static/style.css
**Description:** Main stylesheet for the application.

```css
[from app/static/style.css: lines 1-270, full content, as previously read]
```

### app/static/js/common/header.js
**Description:** JavaScript for header menu interactions.

```javascript
function toggleUserDropdown() {
    var dropdown = document.querySelector('.user-dropdown');
    dropdown.classList.toggle('active');
}
window.onclick = function(event) {
    if (!event.target.closest('.user-dropdown')) {
        var dropdown = document.querySelector('.user-dropdown');
        if (dropdown) dropdown.classList.remove('active');
    }
}
```

---

## Database Schemas
SQL files that define the database structure and initial data.

### database/schema.sql
**Description:** Main database schema (tables, constraints, etc.).

```sql
[from database/schema.sql: lines 1-292, full content, as previously read]
```

### database/persons.sql
**Description:** Person-related data and structure (first 200 lines shown, file truncated for brevity).

```sql
[from database/persons.sql: lines 1-200, file truncated]
```

---

## Python Package Initialization
- **app/__init__.py**: Marks the `app` directory as a Python package.

```python
# This file marks the 'app' directory as a Python package.

```

---

## Application Entry Point
- **app/main.py**: FastAPI application setup, middleware, and router inclusion.

```python
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

```

---

For more details, see the code in each file or refer to the relevant section above. This structure should help you quickly locate and understand the purpose of each part of the codebase. 