# Academic Session Management Module

The Academic Session Management module organizes academic sessions/semesters, including session creation, activation, and scheduling. This module allows administrators to manage academic terms with start and end dates.

## Session List Screen

**File Paths:**
- Route: `app/pages/academic.py` (list_sessions function)
- Template: `app/templates/academic/sessions_list.html`
- Service: `app/services/academic_service.py`

**Description:**
Administrators can view all academic sessions in the system with their dates and status.

**Displayed Information:**
- Session Name
- Start Date
- End Date
- Status (Active/Inactive)

**Links:**
- **Add Session**: Navigates to session creation form
- **Edit**: Opens edit form for specific session
- **Delete**: Removes session from system (with confirmation)

**Pre-conditions:**
- User must have Administrator role
- User must be logged in

**Post-conditions:**
- Displays all sessions in system

## Add Session Screen

**File Paths:**
- Route: `app/pages/academic.py` (add_session_form, add_session functions)
- Template: `app/templates/academic/session_add.html`
- Service: `app/services/academic_service.py`

**Description:**
Administrators can create new academic sessions with name, dates, and status.

**Fields:**
- **Session Name**: Descriptive name for the session (e.g., "Fall 2024", "Spring 2025")
- **Start Date**: Date picker for session start date
- **End Date**: Date picker for session end date
- **Active**: Checkbox to set session as active (default: checked)

**Buttons:**
- **Add Session**: Creates the new session
- **Cancel**: Returns to session list

**Validations:**
- Session name is required
- Start date is required
- End date is required
- End date must be after start date
- Session name should be unique

**Pre-conditions:**
- User must have Administrator role

**Post-conditions:**
- New session is created in database
- Session status is set
- Redirects to session list

## Edit Session Screen

**File Paths:**
- Route: `app/pages/academic.py` (edit_session_form, edit_session functions)
- Template: `app/templates/academic/session_edit.html`
- Service: `app/services/academic_service.py`

**Description:**
Administrators can modify existing session information including dates and status.

**Fields:**
- **Session Name**: Editable session name
- **Start Date**: Editable start date
- **End Date**: Editable end date
- **Active**: Checkbox to toggle session status

**Buttons:**
- **Update Session**: Saves changes to session
- **Cancel**: Returns to session list

**Validations:**
- Session name is required
- Start date is required
- End date is required
- End date must be after start date
- Session name should be unique (if changed)

**Pre-conditions:**
- Session must exist in system
- User must have Administrator role

**Post-conditions:**
- Session information is updated
- Session status is updated
- Redirects to session list

## Session Deletion

**File Paths:**
- Route: `app/pages/academic.py` (delete_session function)
- Service: `app/services/academic_service.py`

**Description:**
Administrators can remove academic sessions from the system.

**Pre-conditions:**
- Session must exist in system
- User must have Administrator role
- Session should not be referenced by active course offerings

**Post-conditions:**
- Session is permanently deleted from database
- Redirects to session list

**Note:** Session deletion should be used carefully as it may affect existing course offerings and student registrations. 