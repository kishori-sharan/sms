# Registration Management Module

The Registration Management module enables students to register for available course offerings and allows administrators to track enrollments. This module handles the enrollment process with capacity checking and registration tracking.

## Student Registration Screen

**File Paths:**
- Route: `app/pages/academic.py` (student_registration_form function)
- Template: `app/templates/academic/student_registration.html`
- Service: `app/services/academic_service.py`

**Description:**
Students can view available courses for registration and enroll in courses for the selected session.

**Fields:**
- **Session Filter**: Dropdown to select academic session for registration

**Displayed Information for Each Course:**
- Course Code and Name
- Session Name
- Faculty Name
- Credits
- Available Seats
- Course Description

**Buttons:**
- **Register for this Course**: Enrolls student in selected course

**Validations:**
- Student must not be already registered for the course
- Course must have available seats
- Course offering must be active
- Student must have Student role

**Pre-conditions:**
- User must have Student role
- User must be logged in
- Active course offerings must exist

**Post-conditions:**
- Student is registered for selected course
- Course enrollment count is updated
- Redirects to student courses page

## Student Courses Screen

**File Paths:**
- Route: `app/pages/academic.py` (student_courses function)
- Template: `app/templates/academic/student_courses.html`
- Service: `app/services/academic_service.py`

**Description:**
Students can view their enrolled courses with filtering by session.

**Displayed Information:**
- Course Code and Name
- Session Name
- Faculty Name
- Credits
- Registration Date
- Course Status (Registered/Completed/Dropped)

**Filters:**
- **Session Filter**: Dropdown to filter courses by specific session

**Links:**
- **Drop Course**: Removes student from course enrollment
- **Register for Courses**: Navigates to registration page

**Pre-conditions:**
- User must have Student role
- User must be logged in

**Post-conditions:**
- Displays student's enrolled courses (filtered by session if selected)

## Course Drop Functionality

**File Paths:**
- Route: `app/pages/academic.py` (drop_course function)
- Service: `app/services/academic_service.py`

**Description:**
Students can drop courses they are enrolled in.

**Pre-conditions:**
- Student must be registered for the course
- User must have Student role
- Registration must exist in system

**Post-conditions:**
- Student registration is removed
- Course enrollment count is decreased
- Redirects to student courses page

## Faculty Course Details Screen

**File Paths:**
- Route: `app/pages/academic.py` (faculty_course_details function)
- Template: `app/templates/academic/faculty_course_details.html`
- Service: `app/services/academic_service.py`

**Description:**
Faculty can view detailed information about their assigned courses including enrolled students.

**Displayed Information:**
- Course Code and Name
- Session Name
- Credits
- Student Count (Current/Maximum)

**Student List:**
- Student Name
- Student Username
- Registration Date

**Links:**
- **View Marks**: Opens student marks management for specific student

**Pre-conditions:**
- User must have Faculty role
- User must be logged in
- Faculty must have assigned courses

**Post-conditions:**
- Displays course details and enrolled students

## Faculty Dashboard Screen

**File Paths:**
- Route: `app/pages/academic.py` (faculty_dashboard function)
- Template: `app/templates/academic/faculty_dashboard.html`
- Service: `app/services/academic_service.py`

**Description:**
Faculty can view an overview of all their assigned course offerings.

**Displayed Information:**
- Course Code and Name
- Session Name
- Student Count (Current/Maximum)
- Credits

**Links:**
- **View Course Details**: Opens detailed course view with student list

**Pre-conditions:**
- User must have Faculty role
- User must be logged in

**Post-conditions:**
- Displays all faculty's assigned courses

## Registration Validation

**File Paths:**
- Route: `app/pages/academic.py` (register_for_course function)
- Service: `app/services/academic_service.py`

**Description:**
System validates course registration requests and handles enrollment.

**Validations:**
- Student must not be already registered for the course
- Course must have available seats
- Course offering must be active
- Student must have Student role
- Registration date is automatically set to current date

**Pre-conditions:**
- Course offering must exist
- Student must exist in system
- User must have Student role

**Post-conditions:**
- Student registration is created
- Course enrollment count is incremented
- Success or error message is displayed 