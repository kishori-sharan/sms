# Course Offering Management Module

The Course Offering Management module manages which courses are offered in each session, assigns faculty, and sets enrollment limits. This module connects courses, sessions, and faculty to create specific course offerings.

## Course Offerings List Screen

**File Paths:**
- Route: `app/pages/academic.py` (list_offerings function)
- Template: `app/templates/academic/offerings_list.html`
- Service: `app/services/academic_service.py`

**Description:**
Administrators can view all course offerings with filtering by session.

**Displayed Information:**
- Course (Code and Name)
- Session Name
- Faculty Name
- Student Count (Current/Maximum)
- Status (Active/Inactive)

**Filters:**
- **Session Filter**: Dropdown to filter offerings by specific session

**Links:**
- **Add Offering**: Navigates to offering creation form
- **Edit**: Opens edit form for specific offering
- **Delete**: Removes offering from system (with confirmation)

**Pre-conditions:**
- User must have Administrator role
- User must be logged in

**Post-conditions:**
- Displays all course offerings (filtered by session if selected)

## Add Course Offering Screen

**File Paths:**
- Route: `app/pages/academic.py` (add_offering_form, add_offering functions)
- Template: `app/templates/academic/offering_add.html`
- Service: `app/services/academic_service.py`

**Description:**
Administrators can create new course offerings by selecting session, course, faculty, and setting enrollment limits.

**Fields:**
- **Academic Session**: Dropdown to select active session
- **Course**: Dropdown to select active course
- **Faculty**: Dropdown to select faculty member
- **Maximum Students**: Number input for enrollment limit (default: 50)

**Buttons:**
- **Add Offering**: Creates the new course offering
- **Cancel**: Returns to offerings list

**Validations:**
- Session is required and must be active
- Course is required and must be active
- Faculty is required and must have Faculty role
- Maximum students must be between 1 and 200
- Combination of session and course should be unique

**Pre-conditions:**
- User must have Administrator role
- Active sessions must exist
- Active courses must exist
- Faculty members must exist

**Post-conditions:**
- New course offering is created
- Current students count is initialized to 0
- Offering is set to active by default
- Redirects to offerings list

## Edit Course Offering Screen

**File Paths:**
- Route: `app/pages/academic.py` (edit_offering_form, edit_offering functions)
- Template: `app/templates/academic/offering_edit.html`
- Service: `app/services/academic_service.py`

**Description:**
Administrators can modify existing course offerings including faculty assignment and enrollment limits.

**Fields:**
- **Academic Session**: Editable session selection
- **Course**: Editable course selection
- **Faculty**: Editable faculty selection
- **Maximum Students**: Editable enrollment limit
- **Active**: Checkbox to toggle offering status

**Buttons:**
- **Update Offering**: Saves changes to offering
- **Cancel**: Returns to offerings list

**Validations:**
- Session is required and must be active
- Course is required and must be active
- Faculty is required and must have Faculty role
- Maximum students must be between 1 and 200
- Maximum students cannot be less than current enrolled students
- Combination of session and course should be unique (if changed)

**Pre-conditions:**
- Course offering must exist in system
- User must have Administrator role

**Post-conditions:**
- Course offering information is updated
- Offering status is updated
- Redirects to offerings list

## Offering Deletion

**File Paths:**
- Route: `app/pages/academic.py` (delete_offering function)
- Service: `app/services/academic_service.py`

**Description:**
Administrators can remove course offerings from the system.

**Pre-conditions:**
- Course offering must exist in system
- User must have Administrator role
- Offering should not have enrolled students

**Post-conditions:**
- Course offering is permanently deleted from database
- Redirects to offerings list

**Note:** Offering deletion should be used carefully as it may affect student registrations and faculty assignments. 