from app.services.db_service import DBService

class AcademicService:
    @staticmethod
    def get_all_sessions():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM academic_sessions ORDER BY start_date DESC')
        sessions = cursor.fetchall()
        cursor.close()
        conn.close()
        return sessions

    @staticmethod
    def get_active_sessions():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM academic_sessions WHERE is_active = TRUE ORDER BY start_date DESC')
        sessions = cursor.fetchall()
        cursor.close()
        conn.close()
        return sessions

    @staticmethod
    def get_session(session_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM academic_sessions WHERE id = %s', (session_id,))
        session = cursor.fetchone()
        cursor.close()
        conn.close()
        return session

    @staticmethod
    def add_session(name, start_date, end_date, is_active=True):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO academic_sessions (name, start_date, end_date, is_active) VALUES (%s, %s, %s, %s)',
            (name, start_date, end_date, is_active)
        )
        session_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return session_id

    @staticmethod
    def update_session(session_id, name, start_date, end_date, is_active):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE academic_sessions SET name=%s, start_date=%s, end_date=%s, is_active=%s WHERE id=%s',
            (name, start_date, end_date, is_active, session_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_session(session_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM academic_sessions WHERE id = %s', (session_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all_courses():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM courses ORDER BY code')
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        return courses

    @staticmethod
    def get_active_courses():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM courses WHERE is_active = TRUE ORDER BY code')
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        return courses

    @staticmethod
    def get_course(course_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM courses WHERE id = %s', (course_id,))
        course = cursor.fetchone()
        cursor.close()
        conn.close()
        return course

    @staticmethod
    def add_course(code, name, description, credits=3):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO courses (code, name, description, credits) VALUES (%s, %s, %s, %s)',
            (code, name, description, credits)
        )
        course_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return course_id

    @staticmethod
    def update_course(course_id, code, name, description, credits, is_active):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE courses SET code=%s, name=%s, description=%s, credits=%s, is_active=%s WHERE id=%s',
            (code, name, description, credits, is_active, course_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_course(course_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM courses WHERE id = %s', (course_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_course_offerings(session_id=None):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        if session_id:
            cursor.execute('''
                SELECT co.*, c.code, c.name as course_name, c.credits, 
                       s.name as session_name, 
                       CONCAT(p.first_name, ' ', p.last_name) as faculty_name
                FROM course_offerings co
                JOIN courses c ON co.course_id = c.id
                JOIN academic_sessions s ON co.session_id = s.id
                JOIN users u ON co.faculty_id = u.id
                JOIN person p ON u.person_id = p.id
                WHERE co.session_id = %s AND co.is_active = TRUE
                ORDER BY c.code
            ''', (session_id,))
        else:
            cursor.execute('''
                SELECT co.*, c.code, c.name as course_name, c.credits, 
                       s.name as session_name, 
                       CONCAT(p.first_name, ' ', p.last_name) as faculty_name
                FROM course_offerings co
                JOIN courses c ON co.course_id = c.id
                JOIN academic_sessions s ON co.session_id = s.id
                JOIN users u ON co.faculty_id = u.id
                JOIN person p ON u.person_id = p.id
                WHERE co.is_active = TRUE
                ORDER BY s.start_date DESC, c.code
            ''')
        offerings = cursor.fetchall()
        cursor.close()
        conn.close()
        return offerings

    @staticmethod
    def get_faculty_offerings(faculty_id, session_id=None):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        if session_id:
            cursor.execute('''
                SELECT co.*, c.code, c.name as course_name, c.credits, 
                       s.name as session_name
                FROM course_offerings co
                JOIN courses c ON co.course_id = c.id
                JOIN academic_sessions s ON co.session_id = s.id
                WHERE co.faculty_id = %s AND co.session_id = %s AND co.is_active = TRUE
                ORDER BY c.code
            ''', (faculty_id, session_id))
        else:
            cursor.execute('''
                SELECT co.*, c.code, c.name as course_name, c.credits, 
                       s.name as session_name
                FROM course_offerings co
                JOIN courses c ON co.course_id = c.id
                JOIN academic_sessions s ON co.session_id = s.id
                WHERE co.faculty_id = %s AND co.is_active = TRUE
                ORDER BY s.start_date DESC, c.code
            ''', (faculty_id,))
        offerings = cursor.fetchall()
        cursor.close()
        conn.close()
        return offerings

    @staticmethod
    def add_course_offering(session_id, course_id, faculty_id, max_students=50):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO course_offerings (session_id, course_id, faculty_id, max_students) VALUES (%s, %s, %s, %s)',
            (session_id, course_id, faculty_id, max_students)
        )
        offering_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return offering_id

    @staticmethod
    def update_course_offering(offering_id, session_id, course_id, faculty_id, max_students, is_active):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE course_offerings SET session_id=%s, course_id=%s, faculty_id=%s, max_students=%s, is_active=%s WHERE id=%s',
            (session_id, course_id, faculty_id, max_students, is_active, offering_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_course_offering(offering_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM course_offerings WHERE id = %s', (offering_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_student_registrations(student_id, session_id=None):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        if session_id:
            cursor.execute('''
                SELECT sr.*, c.code, c.name as course_name, c.credits,
                       s.name as session_name, co.max_students,
                       CONCAT(p.first_name, ' ', p.last_name) as faculty_name
                FROM student_registrations sr
                JOIN course_offerings co ON sr.offering_id = co.id
                JOIN courses c ON co.course_id = c.id
                JOIN academic_sessions s ON co.session_id = s.id
                JOIN users u ON co.faculty_id = u.id
                JOIN person p ON u.person_id = p.id
                WHERE sr.student_id = %s AND co.session_id = %s
                ORDER BY c.code
            ''', (student_id, session_id))
        else:
            cursor.execute('''
                SELECT sr.*, c.code, c.name as course_name, c.credits,
                       s.name as session_name, co.max_students,
                       CONCAT(p.first_name, ' ', p.last_name) as faculty_name
                FROM student_registrations sr
                JOIN course_offerings co ON sr.offering_id = co.id
                JOIN courses c ON co.course_id = c.id
                JOIN academic_sessions s ON co.session_id = s.id
                JOIN users u ON co.faculty_id = u.id
                JOIN person p ON u.person_id = p.id
                WHERE sr.student_id = %s
                ORDER BY s.start_date DESC, c.code
            ''', (student_id,))
        registrations = cursor.fetchall()
        cursor.close()
        conn.close()
        return registrations

    @staticmethod
    def register_student_for_course(student_id, offering_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if already registered
        cursor.execute('SELECT id FROM student_registrations WHERE student_id = %s AND offering_id = %s', 
                      (student_id, offering_id))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Already registered for this course"
        
        # Check if course is full
        cursor.execute('SELECT current_students, max_students FROM course_offerings WHERE id = %s', (offering_id,))
        offering = cursor.fetchone()
        if offering and int(offering['current_students']) >= int(offering['max_students']):
            cursor.close()
            conn.close()
            return False, "Course is full"
        
        # Register student
        cursor.execute(
            'INSERT INTO student_registrations (student_id, offering_id, registration_date) VALUES (%s, %s, CURDATE())',
            (student_id, offering_id)
        )
        
        # Update current students count
        cursor.execute('UPDATE course_offerings SET current_students = current_students + 1 WHERE id = %s', (offering_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Registration successful"

    @staticmethod
    def drop_course_registration(registration_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get offering_id before deleting
        cursor.execute('SELECT offering_id FROM student_registrations WHERE id = %s', (registration_id,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return False
        
        offering_id = result['offering_id']
        
        # Delete registration
        cursor.execute('DELETE FROM student_registrations WHERE id = %s', (registration_id,))
        
        # Update current students count
        cursor.execute('UPDATE course_offerings SET current_students = current_students - 1 WHERE id = %s', (offering_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def get_course_students(offering_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT sr.*, CONCAT(p.first_name, ' ', p.last_name) as student_name,
                   u.username as student_username
            FROM student_registrations sr
            JOIN users u ON sr.student_id = u.id
            JOIN person p ON u.person_id = p.id
            WHERE sr.offering_id = %s
            ORDER BY p.last_name, p.first_name
        ''', (offering_id,))
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return students

    @staticmethod
    def get_student_marks(student_id, offering_id=None):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        if offering_id:
            cursor.execute('''
                SELECT m.*, c.code, c.name as course_name, sr.offering_id
                FROM marks m
                JOIN student_registrations sr ON m.registration_id = sr.id
                JOIN course_offerings co ON sr.offering_id = co.id
                JOIN courses c ON co.course_id = c.id
                WHERE sr.student_id = %s AND sr.offering_id = %s
                ORDER BY m.assignment_type, m.create_dt
            ''', (student_id, offering_id))
        else:
            cursor.execute('''
                SELECT m.*, c.code, c.name as course_name, sr.offering_id
                FROM marks m
                JOIN student_registrations sr ON m.registration_id = sr.id
                JOIN course_offerings co ON sr.offering_id = co.id
                JOIN courses c ON co.course_id = c.id
                WHERE sr.student_id = %s
                ORDER BY c.code, m.assignment_type, m.create_dt
            ''', (student_id,))
        marks = cursor.fetchall()
        cursor.close()
        conn.close()
        return marks

    @staticmethod
    def get_marks_by_registration(registration_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT m.*, c.code, c.name as course_name, sr.offering_id
            FROM marks m
            JOIN student_registrations sr ON m.registration_id = sr.id
            JOIN course_offerings co ON sr.offering_id = co.id
            JOIN courses c ON co.course_id = c.id
            WHERE m.registration_id = %s
            ORDER BY m.assignment_type, m.create_dt
        ''', (registration_id,))
        marks = cursor.fetchall()
        cursor.close()
        conn.close()
        return marks

    @staticmethod
    def get_registration_info(registration_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT sr.*, 
                   CONCAT(p.first_name, ' ', p.last_name) as student_name,
                   u.username as student_username,
                   c.code as course_code, 
                   c.name as course_name,
                   c.credits,
                   s.name as session_name
            FROM student_registrations sr
            JOIN users u ON sr.student_id = u.id
            JOIN person p ON u.person_id = p.id
            JOIN course_offerings co ON sr.offering_id = co.id
            JOIN courses c ON co.course_id = c.id
            JOIN academic_sessions s ON co.session_id = s.id
            WHERE sr.id = %s
        ''', (registration_id,))
        registration_info = cursor.fetchone()
        cursor.close()
        conn.close()
        return registration_info

    @staticmethod
    def add_mark(registration_id, assignment_type, marks_obtained, total_marks=100.00, remarks=None):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO marks (registration_id, assignment_type, marks_obtained, total_marks, remarks) VALUES (%s, %s, %s, %s, %s)',
            (registration_id, assignment_type, marks_obtained, total_marks, remarks)
        )
        mark_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return mark_id

    @staticmethod
    def update_mark(mark_id, assignment_type, marks_obtained, total_marks, remarks):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE marks SET assignment_type=%s, marks_obtained=%s, total_marks=%s, remarks=%s WHERE id=%s',
            (assignment_type, marks_obtained, total_marks, remarks, mark_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_mark(mark_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM marks WHERE id = %s', (mark_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all_degrees():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM degrees ORDER BY name')
        degrees = cursor.fetchall()
        cursor.close()
        conn.close()
        return degrees

    @staticmethod
    def get_student_degrees(student_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT sd.*, d.name as degree_name, d.abbreviation
            FROM student_degrees sd
            JOIN degrees d ON sd.degree_id = d.id
            WHERE sd.student_id = %s
            ORDER BY sd.enrollment_date DESC
        ''', (student_id,))
        degrees = cursor.fetchall()
        cursor.close()
        conn.close()
        return degrees

    @staticmethod
    def enroll_student_in_degree(student_id, degree_id, expected_completion_date):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO student_degrees (student_id, degree_id, enrollment_date, expected_completion_date) VALUES (%s, %s, CURDATE(), %s)',
            (student_id, degree_id, expected_completion_date)
        )
        enrollment_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return enrollment_id

    @staticmethod
    def get_available_courses_for_registration(student_id, session_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT co.*, c.code, c.name as course_name, c.credits, c.description,
                   CONCAT(p.first_name, ' ', p.last_name) as faculty_name
            FROM course_offerings co
            JOIN courses c ON co.course_id = c.id
            JOIN users u ON co.faculty_id = u.id
            JOIN person p ON u.person_id = p.id
            WHERE co.session_id = %s AND co.is_active = TRUE
            AND co.id NOT IN (
                SELECT offering_id FROM student_registrations 
                WHERE student_id = %s AND status = 'Registered'
            )
            AND co.current_students < co.max_students
            ORDER BY c.code
        ''', (session_id, student_id))
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        return courses 

    @staticmethod
    def get_degree(degree_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM degrees WHERE id = %s', (degree_id,))
        degree = cursor.fetchone()
        cursor.close()
        conn.close()
        return degree

    @staticmethod
    def update_degree(degree_id, name, abbreviation, description, is_active):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE degrees SET name=%s, abbreviation=%s, description=%s, is_active=%s WHERE id=%s',
            (name, abbreviation, description, is_active, degree_id)
        )
        conn.commit()
        cursor.close()
        conn.close() 

    @staticmethod
    def add_degree(name, abbreviation, description, is_active=True):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO degrees (name, abbreviation, description, is_active) VALUES (%s, %s, %s, %s)',
            (name, abbreviation, description, is_active)
        )
        conn.commit()
        cursor.close()
        conn.close() 