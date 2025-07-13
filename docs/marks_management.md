# Marks Management Module

The Marks Management module allows faculty to record and update student marks for assignments, exams, and other assessments. This module provides comprehensive grade tracking and management capabilities.

## Faculty Student Marks Screen

**File Paths:**
- Route: `app/pages/academic.py` (faculty_student_marks function)
- Template: `app/templates/academic/faculty_student_marks.html`
- Service: `app/services/academic_service.py`

**Description:**
Faculty can view and manage marks for a specific student in their course.

**Displayed Information:**
- Registration ID
- Student's existing marks for the course

**Marks Table:**
- Assignment Type
- Marks Obtained
- Total Marks
- Percentage
- Remarks
- Date

**Add Mark Form:**
- **Assignment Type**: Text input for assignment type (e.g., "Midterm", "Final", "Project")
- **Marks Obtained**: Number input for marks earned
- **Total Marks**: Number input for maximum possible marks (default: 100)
- **Remarks**: Text area for additional comments

**Buttons:**
- **Add Mark**: Creates new mark entry for student

**Validations:**
- Assignment type is required
- Marks obtained must be positive number
- Total marks must be positive number
- Marks obtained cannot exceed total marks
- Faculty must be assigned to the course

**Pre-conditions:**
- User must have Faculty role
- User must be logged in
- Student must be registered for faculty's course
- Registration must exist in system

**Post-conditions:**
- New mark is recorded for student
- Mark is associated with registration
- Redirects to same page with updated marks

## Student Marks Screen

**File Paths:**
- Route: `app/pages/academic.py` (student_marks function)
- Template: `app/templates/academic/student_marks.html`
- Service: `app/services/academic_service.py`

**Description:**
Students can view their marks and grades for all enrolled courses.

**Displayed Information:**
- Course Code and Name
- Assignment Type
- Marks Obtained
- Total Marks
- Percentage
- Grade (A/B/C/F based on percentage)
- Remarks

**Filters:**
- **Course Filter**: Optional filter by specific course offering

**Pre-conditions:**
- User must have Student role
- User must be logged in

**Post-conditions:**
- Displays student's marks for all courses

## Mark Entry Process

**File Paths:**
- Route: `app/pages/academic.py` (add_mark function)
- Service: `app/services/academic_service.py`

**Description:**
Faculty can add new mark entries for students in their courses.

**Fields:**
- **Registration ID**: Hidden field identifying student's course registration
- **Assignment Type**: Type of assessment (e.g., "Quiz", "Assignment", "Exam")
- **Marks Obtained**: Numeric value of marks earned
- **Total Marks**: Maximum possible marks (default: 100.0)
- **Remarks**: Optional comments about the assessment

**Validations:**
- Registration ID must be valid
- Assignment type is required
- Marks obtained must be positive number
- Total marks must be positive number
- Marks obtained cannot exceed total marks
- Faculty must be assigned to the course

**Pre-conditions:**
- Student must be registered for faculty's course
- Registration must exist in system
- User must have Faculty role

**Post-conditions:**
- New mark entry is created in database
- Mark is associated with student registration
- Mark creation date is automatically set

## Grade Calculation

**File Paths:**
- Template: `app/templates/academic/student_marks.html`
- Service: `app/services/academic_service.py`

**Description:**
System automatically calculates grades based on marks obtained and total marks.

**Grade Scale:**
- A: 90% and above
- B: 80-89%
- C: 70-79%
- F: Below 70%

**Calculation:**
- Percentage = (Marks Obtained / Total Marks) × 100
- Grade is determined based on percentage thresholds

**Pre-conditions:**
- Marks must have valid obtained and total values

**Post-conditions:**
- Grade is displayed alongside percentage

## Mark Management Features

**File Paths:**
- Service: `app/services/academic_service.py`

**Description:**
System provides comprehensive mark management capabilities.

**Features:**
- **Mark Addition**: Faculty can add new marks for students
- **Mark Update**: Faculty can modify existing marks
- **Mark Deletion**: Faculty can remove incorrect marks
- **Mark History**: All mark entries are tracked with timestamps
- **Multiple Assignment Types**: Support for various assessment types

**Validations:**
- Only assigned faculty can manage marks for their courses
- Marks must be within valid ranges
- Assignment types should be descriptive and consistent

**Pre-conditions:**
- Faculty must be assigned to the course
- Student must be registered for the course

**Post-conditions:**
- Marks are properly recorded and associated with students
- Grade calculations are updated automatically 