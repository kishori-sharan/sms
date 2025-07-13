# Course Management Module

The Course Management module allows administrators to create, edit, and manage courses in the system. This module handles course codes, names, descriptions, credits, and active status for all academic courses.

## Course List Screen

**File Paths:**
- Route: `app/pages/academic.py` (list_courses function)
- Template: `app/templates/academic/courses_list.html`
- Service: `app/services/academic_service.py`

**Description:**
Administrators can view all courses in the system with their basic information and status.

**Displayed Information:**
- Course Code
- Course Name
- Credits
- Status (Active/Inactive)

**Links:**
- **Add Course**: Navigates to course creation form
- **Edit**: Opens edit form for specific course
- **Delete**: Removes course from system (with confirmation)

**Pre-conditions:**
- User must have Administrator role
- User must be logged in

**Post-conditions:**
- Displays all courses in system

## Add Course Screen

**File Paths:**
- Route: `app/pages/academic.py` (add_course_form, add_course functions)
- Template: `app/templates/academic/course_add.html`
- Service: `app/services/academic_service.py`

**Description:**
Administrators can create new courses with course code, name, description, and credit information.

**Fields:**
- **Course Code**: Unique identifier for the course (e.g., CS101)
- **Course Name**: Full name of the course (e.g., Introduction to Computer Science)
- **Description**: Detailed description of course content and objectives
- **Credits**: Number of credit hours (default: 3)

**Buttons:**
- **Add Course**: Creates the new course
- **Cancel**: Returns to course list

**Validations:**
- Course code is required and must be unique
- Course name is required
- Credits must be between 1 and 10
- Description is optional but recommended

**Pre-conditions:**
- User must have Administrator role

**Post-conditions:**
- New course is created in database
- Course is set to active by default
- Redirects to course list

## Edit Course Screen

**File Paths:**
- Route: `app/pages/academic.py` (edit_course_form, edit_course functions)
- Template: `app/templates/academic/course_edit.html`
- Service: `app/services/academic_service.py`

**Description:**
Administrators can modify existing course information including status.

**Fields:**
- **Course Code**: Editable unique identifier
- **Course Name**: Editable full name
- **Description**: Editable detailed description
- **Credits**: Editable credit hours (1-10)
- **Active**: Checkbox to toggle course status

**Buttons:**
- **Update Course**: Saves changes to course
- **Cancel**: Returns to course list

**Validations:**
- Course code must be unique (if changed)
- Course name is required
- Credits must be between 1 and 10
- Description is optional

**Pre-conditions:**
- Course must exist in system
- User must have Administrator role

**Post-conditions:**
- Course information is updated
- Course status is updated
- Redirects to course list

## Course Deletion

**File Paths:**
- Route: `app/pages/academic.py` (delete_course function)
- Service: `app/services/academic_service.py`

**Description:**
Administrators can remove courses from the system.

**Pre-conditions:**
- Course must exist in system
- User must have Administrator role
- Course should not be referenced by active offerings

**Post-conditions:**
- Course is permanently deleted from database
- Redirects to course list

**Note:** Course deletion should be used carefully as it may affect existing course offerings and student registrations. 