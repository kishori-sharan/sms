# User Management Module

The User Management module handles user accounts, authentication, roles, and access control within the Student Management System. This module allows administrators to create, manage, and maintain user accounts for students, faculty, and other administrative staff.

## Login Screen

The login screen serves as the primary entry point for all users to access the Student Management System. It provides a secure authentication interface with role-based access control. Users must provide their username, password, and select their appropriate role (Administrator, Faculty, or Student) to gain access to the system. The interface is designed with a clean, minimal layout featuring form fields for user credentials and a prominent login button. Upon successful authentication, users are redirected to their role-specific dashboard, while failed login attempts display appropriate error messages while preserving the entered username and role selection.

**Screenshot Caption:** Login screen showing username, password, and role selection fields with login button.

**Components:**
- **Username Field**: Text input field for entering the user's login identifier. This field is required and must match an existing username in the system.
- **Password Field**: Password input field for secure authentication. This field is required and must match the password associated with the username.
- **Role Dropdown**: Selection dropdown with options for Administrator, Faculty, and Student. This field is required and the selected role must match the user's assigned role in the system.
- **Login Button**: Primary action button that submits the authentication form and validates user credentials against the database.

**Pre-conditions:**
- User must have a valid account in the system
- User account must be active
- User must have at least one assigned role

**Post-conditions:**
- Successful login redirects to home dashboard
- Failed login displays error message and preserves username/role
- User session is created with user details including user_id, username, role, first_name, and last_name

## User List Screen

The User List screen provides administrators with a comprehensive view of all user accounts in the system. It displays a tabular format showing user information including usernames, full names, assigned roles, and account status. The screen includes navigation links to add new users and manage existing accounts. Each user entry shows their basic information and provides action buttons for editing or deleting user accounts. The interface is designed to handle large numbers of users efficiently with clear visual indicators for account status.

**Screenshot Caption:** User list screen displaying table of users with their information and action buttons.

**Components:**
- **User Table**: Data table displaying username, full name (first name + last name), assigned roles, and active status for all users in the system.
- **Add User Link**: Navigation link that opens the user creation form for adding new user accounts to the system.
- **Edit Links**: Action links for each user that open edit forms to modify existing user account information, roles, and status.
- **Delete Buttons**: Action buttons for each user that remove user accounts from the system with confirmation dialogs to prevent accidental deletions.

**Pre-conditions:**
- User must have Administrator role
- User must be logged in

**Post-conditions:**
- Displays all users in system
- Provides access to user management functions

## Add User Screen

The Add User screen allows administrators to create new user accounts by selecting existing persons from the database and assigning appropriate roles. The form provides a comprehensive interface for user creation with fields for username, password, person selection, role assignment, and account status. The screen includes validation to ensure unique usernames and proper role assignments. The interface is designed to prevent duplicate accounts and ensure data integrity.

**Screenshot Caption:** Add user form with fields for username, password, person selection, roles, and account status.

**Components:**
- **Username Field**: Text input for creating a unique identifier for the user account. This field is required and must be unique across all users in the system.
- **Password Field**: Password input for setting the initial authentication credentials. This field is required and should meet security requirements.
- **Person Dropdown**: Selection dropdown populated with all existing persons from the database who don't already have user accounts. This field is required and the selected person must exist in the system.
- **Roles Checkboxes**: Multiple checkbox selection for assigning user roles (Administrator, Faculty, Student). At least one role must be selected.
- **Active Checkbox**: Checkbox to set the initial account status as active or inactive. Defaults to active.
- **Add User Button**: Primary action button that creates the new user account and assigns the selected roles.
- **Cancel Button**: Secondary button that returns to the user list without creating a new account.

**Pre-conditions:**
- Person must exist in the system
- User must have Administrator role
- Selected person must not already have a user account

**Post-conditions:**
- New user account is created
- User roles are assigned
- Redirects to user list

## Edit User Screen

The Edit User screen provides administrators with the ability to modify existing user accounts, update role assignments, and change account status. The form pre-populates with current user information and allows for comprehensive updates including password changes, role modifications, and status toggles. The interface includes validation to maintain data integrity and prevent conflicts.

**Screenshot Caption:** Edit user form with pre-populated fields for modifying user account information.

**Components:**
- **Username Field**: Editable text input showing the current username. This field is required and must remain unique if changed.
- **Password Field**: Optional password input for updating authentication credentials. If left blank, the current password remains unchanged.
- **Person Dropdown**: Editable dropdown showing the currently associated person with options to change to other persons in the system. This field is required.
- **Roles Checkboxes**: Multiple checkbox selection showing currently assigned roles with options to modify role assignments. At least one role must remain selected.
- **Active Checkbox**: Checkbox to toggle the user account status between active and inactive.
- **Update User Button**: Primary action button that saves all changes to the user account and role assignments.
- **Cancel Button**: Secondary button that returns to the user list without saving changes.

**Pre-conditions:**
- User account must exist in system
- User must have Administrator role

**Post-conditions:**
- User account information is updated
- User roles are updated
- Redirects to user list

## User Search Screen

The User Search screen provides administrators with advanced filtering capabilities to locate specific users in the system. The interface includes multiple search criteria including username patterns, role filters, and account status filters. The search functionality supports partial text matching and multiple filter combinations to help administrators quickly find the users they need to manage.

**Screenshot Caption:** User search form with fields for username, role, and active status filters.

**Components:**
- **Username Field**: Text input for partial search of usernames. Supports wildcard matching to find users with similar usernames.
- **Role Dropdown**: Filter dropdown to search for users with specific roles (Administrator, Faculty, Student). Optional filter that can be combined with other criteria.
- **Active Status Dropdown**: Filter dropdown to search for users by account status (Active, Inactive, or All). Optional filter for account management.
- **Search Button**: Primary action button that executes the search with the entered criteria and displays matching results.
- **Clear Button**: Secondary button that resets all search fields to their default empty state.

**Pre-conditions:**
- User must have Administrator role

**Post-conditions:**
- Displays search results or empty state
- Shows filtered user list based on search criteria

## User Search Results Screen

The User Search Results screen displays the filtered user results based on the search criteria entered on the search screen. The results are presented in a tabular format showing user information and providing direct access to user management functions. The screen includes the search criteria used and maintains the search context for further filtering or refinement.

**Screenshot Caption:** Search results table showing filtered users with their information and management options.

**Components:**
- **Results Table**: Data table displaying filtered users with columns for username, full name, assigned roles, and active status.
- **Search Criteria Display**: Text showing the search parameters used to generate the current results.
- **Edit Links**: Action links for each user in the results that open edit forms for user account management.
- **Delete Buttons**: Action buttons for each user that remove user accounts with confirmation dialogs.

**Pre-conditions:**
- Search must have been executed
- User must have Administrator role

**Post-conditions:**
- Displays filtered user results
- Provides access to user management functions for results

## Change Password Screen

The Change Password screen allows all authenticated users to update their account passwords for security purposes. The interface includes current password verification to ensure only authorized users can change passwords, along with new password entry and confirmation fields. The screen includes password requirements and validation to ensure strong password selection.

**Screenshot Caption:** Change password form with current password verification and new password entry fields.

**Components:**
- **Current Password Field**: Password input for verifying the user's existing password. This field is required and must match the user's current password in the database.
- **New Password Field**: Password input for entering the new authentication credentials. This field is required and must be different from the current password.
- **Confirm New Password Field**: Password input for confirming the new password to prevent typing errors. This field is required and must exactly match the new password field.
- **Change Password Button**: Primary action button that validates all fields and updates the user's password in the database.
- **Cancel Button**: Secondary button that returns to the profile page without changing the password.

**Pre-conditions:**
- User must be logged in
- User must have a valid account

**Post-conditions:**
- Password is updated in database
- Success message is displayed
- Redirects to profile page 