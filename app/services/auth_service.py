import os
from app.services.db_service import DBService

class AuthService:
    @staticmethod
    def login(username, password, role):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT users.id, users.username, roles.name AS role,
                   person.first_name, person.last_name
            FROM users
            JOIN user_roles ON users.id = user_roles.user_id
            JOIN roles ON roles.id = user_roles.role_id
            JOIN person ON users.person_id = person.id
            WHERE users.username=%s AND users.password=%s AND roles.name=%s AND users.active=TRUE
        ''', (username, password, role))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user