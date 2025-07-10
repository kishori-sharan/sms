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
async def list_offerings(request: Request, session_id: int = Query(None)):
    admin_required(request)
    offerings = AcademicService.get_course_offerings(session_id)
    sessions = AcademicService.get_active_sessions()
    return templates.TemplateResponse("academic/offerings_list.html", {
        "request": request, 
        "offerings": offerings, 
        "sessions": sessions,
        "selected_session": session_id
    })

@router.get("/academic/offerings/add", response_class=HTMLResponse)
async def add_offering_form(request: Request):
    admin_required(request)
    sessions = AcademicService.get_active_sessions()
    courses = AcademicService.get_active_courses()
    faculty = UserService.get_all_people()  # We'll filter for faculty in template
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
    faculty = UserService.get_all_people()
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
    marks = AcademicService.get_student_marks(registration_id)
    return templates.TemplateResponse("academic/faculty_student_marks.html", {
        "request": request, 
        "marks": marks,
        "registration_id": registration_id
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
async def student_courses(request: Request, session_id: int = Query(None)):
    student_required(request)
    student_id = request.session.get("user_id")
    registrations = AcademicService.get_student_registrations(student_id, session_id)
    sessions = AcademicService.get_active_sessions()
    return templates.TemplateResponse("academic/student_courses.html", {
        "request": request, 
        "registrations": registrations,
        "sessions": sessions,
        "selected_session": session_id
    })

@router.get("/student/registration", response_class=HTMLResponse)
async def student_registration_form(request: Request, session_id: int = Query(None)):
    student_required(request)
    student_id = request.session.get("user_id")
    available_courses = AcademicService.get_available_courses_for_registration(student_id, session_id)
    sessions = AcademicService.get_active_sessions()
    return templates.TemplateResponse("academic/student_registration.html", {
        "request": request, 
        "available_courses": available_courses,
        "sessions": sessions,
        "selected_session": session_id
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
    # This would need to be implemented in AcademicService
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