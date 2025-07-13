# Database Modules

The Student Management System (SMS) database consists of the following modules and tables, organized by functional areas. The entity-relationship diagram for the database is shown in Figure 1.

**Figure 1: Entity Relationship Diagram for the SMS**

[Your screenshot of the MySQL Workbench model would be inserted here]

The database architecture follows a modular design approach with clear separation of concerns across different functional domains. Each module encapsulates related data entities and their relationships, ensuring data integrity and maintainability. The diagram illustrates the primary and foreign key relationships between tables, demonstrating the normalized structure that supports efficient data retrieval and storage operations.

The system employs a three-tier architecture where the database layer provides persistent storage for all application data, including user management, academic records, and administrative functions. The entity-relationship model ensures referential integrity through foreign key constraints while maintaining flexibility for future enhancements and modifications to the system requirements.

## User Management Module

### Roles Table
**Purpose:** Defines system roles and permissions
**Key Fields:**
- `id`: Primary key
- `name`: Role name (Administrator, Faculty, Student)
- `create_dt`, `last_update_dt`: Audit timestamps

**Relationships:**
- Referenced by `user_roles` table

### Users Table
**Purpose:** Stores user account information and authentication details
**Key Fields:**
- `id`: Primary key
- `username`: Unique login username
- `password`: Encrypted password
- `person_id`: Foreign key to person table
- `active`: Account status (TRUE/FALSE)

**Relationships:**
- References `person` table
- Referenced by `user_roles`, `course_offerings`, `student_registrations`, `student_degrees`

### User_Roles Table
**Purpose:** Many-to-many relationship between users and roles
**Key Fields:**
- `user_id`: Foreign key to users table
- `role_id`: Foreign key to roles table
- Composite primary key (user_id, role_id)

**Relationships:**
- References `users` and `roles` tables

## Person Management Module

### Person Table
**Purpose:** Stores personal information for all system users
**Key Fields:**
- `id`: Primary key
- `first_name`, `last_name`: Person's name
- `birth_date`: Date of birth
- `gender`: ENUM (Male, Female, Other)

**Relationships:**
- Referenced by `users`, `addresses`, `contact_info` tables

### Addresses Table
**Purpose:** Stores multiple addresses per person
**Key Fields:**
- `id`: Primary key
- `person_id`: Foreign key to person table
- `address_type`: ENUM (Home, Work, School, Other)
- `address_line1`, `address_line2`: Address components
- `city`, `state`, `postal_code`, `country`: Location details
- `is_active`: Address status

**Relationships:**
- References `person` table

### Contact_Info Table
**Purpose:** Stores multiple contact methods per person
**Key Fields:**
- `id`: Primary key
- `person_id`: Foreign key to person table
- `contact_type`: ENUM (Phone, Email, Other)
- `contact_value`: Contact information
- `is_active`: Contact status

**Relationships:**
- References `person` table

## Academic Management Module

### Academic_Sessions Table
**Purpose:** Defines academic terms/semesters
**Key Fields:**
- `id`: Primary key
- `name`: Session name (e.g., "Fall 2024")
- `start_date`, `end_date`: Session period
- `is_active`: Session status

**Relationships:**
- Referenced by `course_offerings` table

### Courses Table
**Purpose:** Defines available courses in the system
**Key Fields:**
- `id`: Primary key
- `code`: Unique course code (e.g., "CS101")
- `name`: Course title
- `description`: Course description
- `credits`: Credit hours (default 3)
- `is_active`: Course status

**Relationships:**
- Referenced by `course_offerings` table

### Course_Offerings Table
**Purpose:** Links courses to specific academic sessions with faculty assignments
**Key Fields:**
- `id`: Primary key
- `session_id`: Foreign key to academic_sessions
- `course_id`: Foreign key to courses
- `faculty_id`: Foreign key to users (faculty member)
- `max_students`: Enrollment limit
- `current_students`: Current enrollment count
- `is_active`: Offering status

**Relationships:**
- References `academic_sessions`, `courses`, `users` tables
- Referenced by `student_registrations` table

## Registration Management Module

### Student_Registrations Table
**Purpose:** Tracks student course enrollments
**Key Fields:**
- `id`: Primary key
- `student_id`: Foreign key to users table
- `offering_id`: Foreign key to course_offerings
- `registration_date`: Enrollment date
- `status`: ENUM (Registered, Dropped, Completed)
- Unique constraint on (student_id, offering_id)

**Relationships:**
- References `users` and `course_offerings` tables
- Referenced by `marks` table

## Academic Assessment Module

### Marks Table
**Purpose:** Stores student grades and assessment results
**Key Fields:**
- `id`: Primary key
- `registration_id`: Foreign key to student_registrations
- `assignment_type`: ENUM (Midterm, Final, Assignment, Project, Participation)
- `marks_obtained`: Score achieved
- `total_marks`: Maximum possible score (default 100.00)
- `percentage`: Computed percentage (generated column)
- `grade`: Computed letter grade (generated column)
- `remarks`: Additional comments

**Computed Fields:**
- `percentage`: (marks_obtained / total_marks) * 100
- `grade`: Letter grade based on percentage:
  - A+ (90%+), A (80-89%), B+ (70-79%), B (60-69%)
  - C+ (50-59%), C (40-49%), D (35-39%), F (<35%)

**Relationships:**
- References `student_registrations` table

## Degree Management Module

### Degrees Table
**Purpose:** Defines degree programs offered by the institution
**Key Fields:**
- `id`: Primary key
- `name`: Full degree name
- `abbreviation`: Short form (e.g., "B.Tech CS")
- `description`: Degree description
- `is_active`: Degree status

**Relationships:**
- Referenced by `student_degrees` table

### Student_Degrees Table
**Purpose:** Tracks student enrollment in degree programs
**Key Fields:**
- `id`: Primary key
- `student_id`: Foreign key to users table
- `degree_id`: Foreign key to degrees table
- `enrollment_date`: When student enrolled
- `expected_completion_date`: Target completion date
- `actual_completion_date`: Actual completion date
- `status`: ENUM (Enrolled, In Progress, Completed, Dropped)

**Relationships:**
- References `users` and `degrees` tables

## Database Design Principles

### Audit Trail
All tables include audit fields:
- `create_dt`: Record creation timestamp
- `last_update_dt`: Last modification timestamp

### Referential Integrity
- Foreign key constraints ensure data consistency
- Cascade rules prevent orphaned records
- Unique constraints prevent duplicate entries

### Data Types
- **ENUMs**: Used for status fields and categories
- **DECIMAL**: Used for marks and percentages (precision 5, scale 2)
- **DATE**: Used for dates without time
- **DATETIME**: Used for timestamps
- **TEXT**: Used for long descriptions
- **VARCHAR**: Used for variable-length strings

### Indexing Strategy
- Primary keys are auto-incrementing integers
- Foreign keys are indexed for performance
- Unique constraints create indexes automatically
- Composite unique keys for business rules

## Sample Data

The schema includes comprehensive sample data:
- **3 Roles**: Administrator, Faculty, Student
- **8 Persons**: Mix of students, faculty, and administrators
- **8 Users**: Linked to persons with appropriate roles
- **3 Academic Sessions**: Fall 2024, Spring 2025, Summer 2025
- **4 Degrees**: B.Tech CS, B.Tech IT, M.Tech CS, B.Sc Math
- **8 Courses**: CS101, CS201, CS301, CS401, IT101, MATH101, MATH201, CS501
- **10 Course Offerings**: Courses assigned to sessions and faculty
- **5 Student Degree Enrollments**: Students enrolled in degree programs
- **Addresses and Contact Info**: Sample data for all persons

## Database File Location
**Schema File:** `database/schema.sql`
- Contains all table definitions
- Includes sample data inserts
- Can be executed to create complete database structure 