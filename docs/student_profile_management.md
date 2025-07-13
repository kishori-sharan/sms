# Student Profile Management Module

The Student Profile Management module handles personal information, addresses, and contact details for all students and users in the system. This module provides comprehensive management of personal data with support for multiple addresses and contact methods.

## Person Search Screen

The Person Search screen provides administrators with advanced search capabilities to locate specific persons in the system. The interface includes multiple search criteria such as first name, last name, birth date, gender, and role filters. The search functionality supports partial text matching for names and exact matching for dates and gender. The screen is designed to help administrators quickly find persons for profile management, user account creation, or data updates. The search results can be filtered and sorted to efficiently manage large datasets of personal information.

**Screenshot Caption:** Person search form with fields for first name, last name, birth date, gender, and role filters.

**Components:**
- **First Name Field**: Text input for partial search of first names. Supports wildcard matching to find persons with similar first names.
- **Last Name Field**: Text input for partial search of last names. Supports wildcard matching to find persons with similar last names.
- **Birth Date Field**: Date picker for exact birth date search. Allows administrators to find persons born on specific dates.
- **Gender Dropdown**: Filter dropdown to search for persons by gender (Male, Female, Other). Optional filter for demographic searches.
- **Role Dropdown**: Filter dropdown to search for persons with specific user roles (Administrator, Faculty, Student, or None). Optional filter for role-based searches.
- **Search Button**: Primary action button that executes the search with the entered criteria and displays matching results.
- **Clear Button**: Secondary button that resets all search fields to their default empty state.

**Pre-conditions:**
- User must have Administrator role
- User must be logged in

**Post-conditions:**
- Displays search results or empty state
- Shows filtered person list based on search criteria

## Person Search Results Screen

The Person Search Results screen displays the filtered person results based on the search criteria entered on the search screen. The results are presented in a tabular format showing person information with pagination and sorting options. Each person entry displays their basic information and provides direct access to detailed views and editing functions. The screen maintains search context and allows for further refinement of results.

**Screenshot Caption:** Search results table showing filtered persons with their information and management options.

**Components:**
- **Results Table**: Data table displaying filtered persons with columns for first name, last name, birth date, gender, and role (if assigned).
- **Search Criteria Display**: Text showing the search parameters used to generate the current results.
- **View Details Links**: Action links for each person that open detailed person view pages with comprehensive information.
- **Edit Links**: Action links for each person that open edit forms for modifying personal information.

**Pre-conditions:**
- Search must have been executed
- User must have Administrator role

**Post-conditions:**
- Displays filtered person results
- Provides access to person management functions for results

## Add Person Screen

The Add Person screen allows administrators to create new person records with comprehensive personal information, addresses, and contact details. The form provides a structured interface for entering basic personal data along with optional address and contact information. The screen includes validation to ensure data integrity and supports adding multiple addresses and contact methods for each person. The interface is designed to capture complete personal profiles efficiently.

**Screenshot Caption:** Add person form with fields for personal information, addresses, and contact details.

**Components:**
- **First Name Field**: Text input for entering the person's first name. This field is required and should contain the person's legal first name.
- **Last Name Field**: Text input for entering the person's last name. This field is required and should contain the person's legal last name.
- **Birth Date Field**: Date picker for selecting the person's date of birth. This field is required and must be a valid date.
- **Gender Dropdown**: Selection dropdown with options for Male, Female, and Other. This field is required for demographic data collection.
- **Address Type Dropdown**: Selection dropdown for address type (Home, Work, School, Other). Optional field for categorizing addresses.
- **Address Line 1 Field**: Text input for the primary address line. Required if address information is provided.
- **Address Line 2 Field**: Text input for secondary address line (apartment number, unit, etc.). Optional field for additional address details.
- **City Field**: Text input for the city name. Required if address information is provided.
- **State Field**: Text input for state or province name. Required if address information is provided.
- **Postal Code Field**: Text input for postal or ZIP code. Required if address information is provided.
- **Country Field**: Text input for country name. Required if address information is provided.
- **Contact Type Dropdown**: Selection dropdown for contact type (Phone, Email, Other). Optional field for categorizing contact information.
- **Contact Value Field**: Text input for contact information value (phone number, email address, etc.). Required if contact type is selected.
- **Add Person Button**: Primary action button that creates the new person record with all associated addresses and contacts.
- **Cancel Button**: Secondary button that returns to the person list without creating a new record.

**Pre-conditions:**
- User must have Administrator role

**Post-conditions:**
- New person record is created
- Associated addresses and contacts are created
- Redirects to person details page

## Person Details Screen

The Person Details screen provides a comprehensive view of person information with a tabbed interface for organizing different types of data. The screen displays general personal information, associated user account details, multiple addresses, and contact information. Each tab contains relevant information and provides options for adding, editing, or deleting associated data. The interface is designed to give administrators a complete overview of each person's profile and associated accounts.

**Screenshot Caption:** Person details screen with tabbed interface showing general info, user info, addresses, and contacts.

**Components:**
- **General Info Tab**: Tab displaying basic personal information including first name, last name, birth date, and gender in read-only format.
- **User Info Tab**: Tab showing associated user account details including username, active status, assigned roles, and options for user account management.
- **Addresses Tab**: Tab displaying all addresses for the person with address type and full address information, plus options for adding and editing addresses.
- **Contacts Tab**: Tab showing all contact information with contact type and value, plus options for adding and editing contacts.
- **Edit Person Button**: Action button that opens the edit form for modifying basic personal information.
- **Delete Person Button**: Action button that removes the person from the system with confirmation dialog.
- **Add User Button**: Action button that creates a user account for the person if they don't already have one.
- **Edit User Button**: Action button that modifies the associated user account if one exists.
- **Delete User Button**: Action button that removes the user account while keeping the person record.

**Pre-conditions:**
- Person must exist in system
- User must have Administrator role

**Post-conditions:**
- Displays complete person information
- Provides access to person and user management functions

## Edit Person Screen

The Edit Person screen allows administrators to modify basic personal information for existing persons. The form pre-populates with current person data and provides a clean interface for making updates. The screen includes validation to ensure data integrity and maintains consistency with the person's existing profile information.

**Screenshot Caption:** Edit person form with pre-populated fields for modifying personal information.

**Components:**
- **First Name Field**: Editable text input showing the current first name. This field is required and should contain the person's legal first name.
- **Last Name Field**: Editable text input showing the current last name. This field is required and should contain the person's legal last name.
- **Birth Date Field**: Editable date picker showing the current birth date. This field is required and must be a valid date.
- **Gender Dropdown**: Editable dropdown showing the current gender selection with options for Male, Female, and Other. This field is required.
- **Update Person Button**: Primary action button that saves all changes to the person record.
- **Cancel Button**: Secondary button that returns to the previous page without saving changes.

**Pre-conditions:**
- Person must exist in system
- User must have Administrator role

**Post-conditions:**
- Person record is updated
- Redirects to specified return page

## Profile Screen

The Profile screen allows users to view their own profile information including personal details, addresses, and contacts. The screen provides a comprehensive overview of the user's personal information and associated data. Users can access their profile information and navigate to related functions such as password changes and profile editing.

**Screenshot Caption:** User profile screen displaying personal information, addresses, and contact details.

**Components:**
- **Personal Information Section**: Display area showing first name, last name, birth date, and gender in read-only format.
- **User Information Section**: Display area showing username, active status, and assigned roles for the current user.
- **Addresses Section**: Display area showing all addresses with type and full address information for the user.
- **Contacts Section**: Display area showing all contact information with type and value for the user.
- **Change Password Link**: Navigation link that opens the password change form for updating account credentials.
- **Edit Profile Link**: Navigation link that opens the edit form for modifying personal information.

**Pre-conditions:**
- User must be logged in

**Post-conditions:**
- Displays user's complete profile information
- Provides access to profile management functions

## Add User for Person Screen

The Add User for Person screen allows administrators to create user accounts for persons who don't already have associated user accounts. The form provides a streamlined interface for user account creation with role assignment and status setting. The screen includes validation to prevent duplicate accounts and ensure proper role assignments.

**Screenshot Caption:** Add user form for creating user account for existing person.

**Components:**
- **Username Field**: Text input for creating a unique identifier for the user account. This field is required and must be unique across all users in the system.
- **Password Field**: Password input for setting the initial authentication credentials. This field is required and should meet security requirements.
- **Roles Checkboxes**: Multiple checkbox selection for assigning user roles (Administrator, Faculty, Student). At least one role must be selected.
- **Active Checkbox**: Checkbox to set the initial account status as active or inactive. Defaults to active.
- **Add User Button**: Primary action button that creates the user account for the person and assigns the selected roles.
- **Cancel Button**: Secondary button that returns to the person details page without creating a user account.

**Pre-conditions:**
- Person must exist in system
- Person must not have existing user account
- User must have Administrator role

**Post-conditions:**
- User account is created for person
- User roles are assigned
- Redirects to person details page

## Edit User for Person Screen

The Edit User for Person screen allows administrators to modify user accounts associated with specific persons. The form pre-populates with current user information and provides options for updating username, password, roles, and account status. The interface includes validation to maintain data integrity and prevent conflicts.

**Screenshot Caption:** Edit user form for modifying user account associated with person.

**Components:**
- **Username Field**: Editable text input showing the current username. This field is required and must remain unique if changed.
- **Password Field**: Optional password input for updating authentication credentials. If left blank, the current password remains unchanged.
- **Roles Checkboxes**: Multiple checkbox selection showing currently assigned roles with options to modify role assignments. At least one role must remain selected.
- **Active Checkbox**: Checkbox to toggle the user account status between active and inactive.
- **Update User Button**: Primary action button that saves all changes to the user account and role assignments.
- **Cancel Button**: Secondary button that returns to the person details page without saving changes.

**Pre-conditions:**
- Person must have associated user account
- User must have Administrator role

**Post-conditions:**
- User account is updated
- User roles are updated
- Redirects to person details page 