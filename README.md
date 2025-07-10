# Student Management System (SMS)

A comprehensive Student Management System built with FastAPI and Jinja2 templates, designed for Indian universities and colleges.

## Features

### 🔐 Authentication & User Management
- **Multi-role Authentication**: Administrator, Faculty, and Student roles
- **Profile Management**: Users can view and update their personal information
- **Password Management**: Secure password change functionality
- **Session Management**: Secure session handling with timeout

### 👥 Personal Information Management
- **Person Records**: Complete personal information tracking
- **Address Management**: Multiple addresses per person (Home, Work, School, Other)
- **Contact Information**: Phone, email, and other contact details
- **User Accounts**: Link persons to user accounts with roles

### 🎓 Academic Management
- **Academic Sessions**: Manage semesters and academic terms
- **Course Management**: Add, edit, and manage courses with credits
- **Course Offerings**: Assign faculty to courses in specific sessions
- **Student Registration**: Students can register for courses
- **Faculty Assignment**: Assign faculty members to teach courses

### 📊 Marks & Grades
- **Grade Tracking**: Comprehensive marks tracking system
- **Assignment Types**: Midterm, Final, Assignment, Project, Participation
- **Automatic Grading**: Automatic grade calculation (A+, A, B+, B, C+, C, D, F)
- **Performance Analytics**: Student performance tracking

### 🎯 Degree Management
- **Degree Programs**: Manage different degree programs
- **Student Enrollments**: Track student degree enrollments
- **Degree Printing**: Generate and print degree certificates
- **Completion Tracking**: Track degree completion status

### 📱 Role-Based Access Control

#### Administrator
- Full access to all system features
- Manage personal information for all users
- Create and manage user accounts
- Manage academic sessions, courses, and offerings
- View system statistics and reports

#### Faculty
- View assigned courses and students
- Manage student marks and grades
- View personal profile and information
- Access to faculty-specific dashboard

#### Student
- View enrolled courses and academic progress
- Register for new courses
- View marks and grades
- Access personal profile
- Print degree certificates

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: MySQL
- **Templates**: Jinja2
- **Styling**: CSS3 with responsive design
- **Authentication**: Session-based with role management

## Database Schema

### Core Tables
- `person`: Personal information
- `users`: User accounts and authentication
- `user_roles`: Role assignments
- `addresses`: Address information
- `contact_info`: Contact details

### Academic Tables
- `academic_sessions`: Academic terms/semesters
- `courses`: Course definitions
- `course_offerings`: Course offerings in sessions
- `student_registrations`: Student course enrollments
- `marks`: Student grades and marks
- `degrees`: Degree programs
- `student_degrees`: Student degree enrollments

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sms
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file with:
   ```
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=student_mgmt
   WEB_SESSION_SECRET_KEY=your_secret_key
   WEB_SESSION_TIMEOUT=3600
   ```

5. **Set up database**
   ```bash
   mysql -u your_username -p < database/schema.sql
   ```

6. **Run the application**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Usage

### Default Login Credentials

#### Administrator
- Username: `admin`
- Password: `password123`
- Role: Administrator

#### Faculty
- Username: `faculty1`
- Password: `password123`
- Role: Faculty

#### Student
- Username: `student1`
- Password: `password123`
- Role: Student

### Key Features by Role

#### For Administrators
1. **User Management**: Navigate to "Manage Users" to create and manage user accounts
2. **Personal Information**: Use "Manage Personal Information" to add/edit person records
3. **Academic Setup**: 
   - Create academic sessions in "Academic Sessions"
   - Add courses in "Course Management"
   - Assign faculty to courses in "Course Offerings"
4. **Degree Management**: Manage degree programs and student enrollments

#### For Faculty
1. **Course Dashboard**: View assigned courses and student lists
2. **Grade Management**: Enter and manage student marks
3. **Profile Management**: Update personal information

#### For Students
1. **Course Registration**: Register for available courses
2. **Academic Progress**: View enrolled courses and grades
3. **Degree Tracking**: Monitor degree program progress
4. **Profile Management**: Update personal information

## API Endpoints

### Authentication
- `GET /`: Login page
- `POST /login`: User authentication
- `GET /logout`: User logout
- `GET /profile`: User profile page
- `GET /change_password`: Change password form
- `POST /change_password`: Update password

### Personal Information (Admin)
- `GET /manage/personal_info`: List all persons
- `GET /manage/personal_info/add`: Add person form
- `POST /manage/personal_info/add`: Create person
- `GET /manage/person/{id}`: Person details
- `POST /manage/person/{id}/edit`: Update person

### User Management (Admin)
- `GET /users`: List all users
- `GET /users/add`: Add user form
- `POST /users/add`: Create user
- `GET /users/{id}/edit`: Edit user form
- `POST /users/{id}/edit`: Update user

### Academic Management (Admin)
- `GET /academic/sessions`: List academic sessions
- `GET /academic/courses`: List courses
- `GET /academic/offerings`: List course offerings
- `GET /academic/degrees`: List degree programs

### Faculty Features
- `GET /faculty/dashboard`: Faculty dashboard
- `GET /faculty/courses/{id}`: Course details
- `POST /faculty/marks/add`: Add student marks

### Student Features
- `GET /student/dashboard`: Student dashboard
- `GET /student/courses`: Enrolled courses
- `GET /student/registration`: Course registration
- `POST /student/register`: Register for course
- `GET /student/marks`: View marks
- `GET /academic/degree/print/{id}`: Print degree

## Security Features

- **Session Management**: Secure session handling with timeout
- **Role-Based Access**: Strict role-based access control
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Protection**: Parameterized queries
- **XSS Protection**: Template escaping

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team or create an issue in the repository.

