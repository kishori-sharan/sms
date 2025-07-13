# Person Management Module

The Person Management module provides administrators with comprehensive tools to manage personal information, addresses, and contact details for all students, faculty, and administrators in the system. This module handles the core personal data management functions that support the entire Student Management System.

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

## Add Address Functionality

The Add Address functionality allows administrators to add new addresses to existing person records. This feature is accessible through the Person Details screen and provides a streamlined interface for adding address information.

**Screenshot Caption:** Add address form for adding new address to person record.

**Components:**
- **Address Type Dropdown**: Selection dropdown for address type (Home, Work, School, Other). This field is required for categorizing the address.
- **Address Line 1 Field**: Text input for the primary address line. This field is required and should contain the main address information.
- **Address Line 2 Field**: Text input for secondary address line (apartment number, unit, etc.). Optional field for additional address details.
- **City Field**: Text input for the city name. This field is required for complete address information.
- **State Field**: Text input for state or province name. This field is required for complete address information.
- **Postal Code Field**: Text input for postal or ZIP code. This field is required for complete address information.
- **Country Field**: Text input for country name. This field is required for complete address information.
- **Add Address Button**: Primary action button that creates the new address record for the person.
- **Cancel Button**: Secondary button that returns to the person details without adding the address.

**Pre-conditions:**
- Person must exist in system
- User must have Administrator role

**Post-conditions:**
- New address is added to person record
- Redirects to person details page

## Add Contact Functionality

The Add Contact functionality allows administrators to add new contact information to existing person records. This feature is accessible through the Person Details screen and provides a streamlined interface for adding contact details.

**Screenshot Caption:** Add contact form for adding new contact information to person record.

**Components:**
- **Contact Type Dropdown**: Selection dropdown for contact type (Phone, Email, Other). This field is required for categorizing the contact information.
- **Contact Value Field**: Text input for contact information value (phone number, email address, etc.). This field is required and should contain the actual contact information.
- **Add Contact Button**: Primary action button that creates the new contact record for the person.
- **Cancel Button**: Secondary button that returns to the person details without adding the contact.

**Pre-conditions:**
- Person must exist in system
- User must have Administrator role

**Post-conditions:**
- New contact is added to person record
- Redirects to person details page

## Person List Screen

The Person List screen provides administrators with a comprehensive view of all persons in the system. It displays a tabular format showing person information including names, birth dates, gender, and associated roles. The screen includes navigation links to add new persons and manage existing records. Each person entry shows their basic information and provides action buttons for viewing details or editing person information.

**Screenshot Caption:** Person list screen displaying table of persons with their information and management options.

**Components:**
- **Person Table**: Data table displaying first name, last name, birth date, gender, and role (if assigned) for all persons in the system.
- **Add Person Link**: Navigation link that opens the person creation form for adding new person records to the system.
- **View Details Links**: Action links for each person that open detailed person view pages with comprehensive information.
- **Edit Links**: Action links for each person that open edit forms to modify existing person information.

**Pre-conditions:**
- User must have Administrator role
- User must be logged in

**Post-conditions:**
- Displays all persons in system
- Provides access to person management functions 