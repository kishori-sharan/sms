# Degree Management Module

The Degree Management module handles degree programs, student degree enrollment, and degree completion tracking. This module allows administrators to manage degree programs and students can view their degree progress.

## Degree Programs List Screen

**File Paths:**
- Route: `app/pages/academic.py` (list_degrees function)
- Template: `app/templates/academic/degrees_list.html`
- Service: `app/services/academic_service.py`

**Description:**
Administrators can view all degree programs in the system with their basic information.

**Displayed Information:**
- Degree Name
- Abbreviation
- Description (truncated if long)
- Status (Active/Inactive)

**Links:**
- **Add Degree**: Navigates to degree creation form
- **Edit**: Opens edit form for specific degree
- **Delete**: Removes degree from system (with confirmation)

**Pre-conditions:**
- User must have Administrator role
- User must be logged in

**Post-conditions:**
- Displays all degree programs in system

## Add Degree Screen

**File Paths:**
- Route: `app/pages/academic.py` (add_degree_form, add_degree functions)
- Template: `app/templates/academic/degree_add.html`
- Service: `app/services/academic_service.py`

**Description:**
Administrators can create new degree programs with name, abbreviation, and description.

**Fields:**
- **Degree Name**: Full name of the degree program (e.g., "Bachelor of Science in Computer Science")
- **Abbreviation**: Short form of degree (e.g., "BSCS")
- **Description**: Detailed description of the degree program

**Buttons:**
- **Add Degree**: Creates the new degree program
- **Cancel**: Returns to degree list

**Validations:**
- Degree name is required
- Abbreviation is required
- Degree name should be unique
- Abbreviation should be unique

**Pre-conditions:**
- User must have Administrator role

**Post-conditions:**
- New degree program is created in database
- Degree is set to active by default
- Redirects to degree list

## Edit Degree Screen

**File Paths:**
- Route: `app/pages/academic.py` (edit_degree_form, edit_degree functions)
- Template: `app/templates/academic/degree_edit.html`
- Service: `app/services/academic_service.py`

**Description:**
Administrators can modify existing degree program information including status.

**Fields:**
- **Degree Name**: Editable full name
- **Abbreviation**: Editable short form
- **Description**: Editable detailed description
- **Active**: Checkbox to toggle degree status

**Buttons:**
- **Update Degree**: Saves changes to degree program
- **Cancel**: Returns to degree list

**Validations:**
- Degree name is required
- Abbreviation is required
- Degree name should be unique (if changed)
- Abbreviation should be unique (if changed)

**Pre-conditions:**
- Degree program must exist in system
- User must have Administrator role

**Post-conditions:**
- Degree program information is updated
- Degree status is updated
- Redirects to degree list

## Student Dashboard Screen

**File Paths:**
- Route: `app/pages/academic.py` (student_dashboard function)
- Template: `app/templates/academic/student_dashboard.html`
- Service: `app/services/academic_service.py`

**Description:**
Students can view their degree programs and academic progress.

**Displayed Information:**
- **Enrolled Courses**: Current course registrations
- **Degree Programs**: Enrolled degree programs with status
- **Quick Actions**: Links to registration, marks, profile, and degree printing

**Degree Information:**
- Degree Name and Abbreviation
- Enrollment Date
- Expected Completion Date
- Actual Completion Date (if completed)
- Status

**Links:**
- **Register for Courses**: Navigates to course registration
- **View Marks**: Opens marks page
- **My Profile**: Opens profile page
- **Print Degree**: Generates degree certificate

**Pre-conditions:**
- User must have Student role
- User must be logged in

**Post-conditions:**
- Displays student's academic overview

## Degree Certificate Print Screen

**File Paths:**
- Route: `app/pages/academic.py` (print_degree function)
- Template: `app/templates/academic/degree_print.html`
- Service: `app/services/academic_service.py`

**Description:**
Students and administrators can generate and print degree certificates.

**Displayed Information:**
- Degree Name and Abbreviation
- Enrollment Status
- Enrollment Date
- Expected Completion Date
- Actual Completion Date (if completed)
- GPA (if available)
- Credits Earned (if available)

**Buttons:**
- **Print Certificate**: Opens print dialog for certificate

**Pre-conditions:**
- User must have Student or Administrator role
- Student must exist in system
- Student must have enrolled degree programs

**Post-conditions:**
- Displays degree certificate information
- Print functionality is available

## Degree Enrollment Process

**File Paths:**
- Service: `app/services/academic_service.py`

**Description:**
System handles student enrollment in degree programs.

**Fields:**
- **Student ID**: Student's user ID
- **Degree ID**: Selected degree program
- **Expected Completion Date**: Target completion date

**Validations:**
- Student must exist in system
- Degree program must exist and be active
- Student must not be already enrolled in the same degree
- Expected completion date must be in the future

**Pre-conditions:**
- Student must have Student role
- Degree program must be active

**Post-conditions:**
- Student is enrolled in degree program
- Enrollment date is automatically set to current date
- Degree status is set to "Enrolled"

## Degree Completion Tracking

**File Paths:**
- Service: `app/services/academic_service.py`

**Description:**
System tracks degree completion status and progress.

**Status Types:**
- **Enrolled**: Student is actively pursuing the degree
- **Completed**: Student has successfully completed the degree
- **Withdrawn**: Student has withdrawn from the degree program

**Tracking Features:**
- **Enrollment Date**: When student started the degree
- **Expected Completion**: Target completion date
- **Actual Completion**: Actual completion date (when completed)
- **GPA Tracking**: Grade point average calculation
- **Credits Earned**: Total credits completed

**Pre-conditions:**
- Student must be enrolled in degree program

**Post-conditions:**
- Degree status is updated appropriately
- Completion information is recorded 