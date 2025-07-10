from app.services.db_service import DBService

class UserService:
    @staticmethod
    def list_users():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT users.id, users.username, users.active, person.first_name, person.last_name,
                   GROUP_CONCAT(roles.name) AS roles
            FROM users
            JOIN person ON users.person_id = person.id
            LEFT JOIN user_roles ON users.id = user_roles.user_id
            LEFT JOIN roles ON user_roles.role_id = roles.id
            GROUP BY users.id
        ''')
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users

    @staticmethod
    def get_user(user_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT users.*, person.first_name, person.last_name,
                   GROUP_CONCAT(roles.name) AS roles
            FROM users
            JOIN person ON users.person_id = person.id
            LEFT JOIN user_roles ON users.id = user_roles.user_id
            LEFT JOIN roles ON user_roles.role_id = roles.id
            WHERE users.id = %s
            GROUP BY users.id
        ''', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def add_user(username, password, person_id, role_ids, active=True):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password, person_id, active)
            VALUES (%s, %s, %s, %s)
        ''', (username, password, person_id, active))
        user_id = cursor.lastrowid
        for role_id in role_ids:
            cursor.execute('INSERT INTO user_roles (user_id, role_id) VALUES (%s, %s)', (user_id, role_id))
        conn.commit()
        cursor.close()
        conn.close()
        return user_id

    @staticmethod
    def update_user(user_id, username, password, person_id, role_ids, active):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        if password:
            cursor.execute('''
                UPDATE users SET username=%s, password=%s, person_id=%s, active=%s WHERE id=%s
            ''', (username, password, person_id, active, user_id))
        else:
            cursor.execute('''
                UPDATE users SET username=%s, person_id=%s, active=%s WHERE id=%s
            ''', (username, person_id, active, user_id))
        cursor.execute('DELETE FROM user_roles WHERE user_id=%s', (user_id,))
        for role_id in role_ids:
            cursor.execute('INSERT INTO user_roles (user_id, role_id) VALUES (%s, %s)', (user_id, role_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_user(user_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM user_roles WHERE user_id=%s', (user_id,))
        cursor.execute('DELETE FROM users WHERE id=%s', (user_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def toggle_active(user_id, active):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET active=%s WHERE id=%s', (active, user_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all_roles():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, name FROM roles')
        roles = cursor.fetchall()
        cursor.close()
        conn.close()
        return roles

    @staticmethod
    def get_all_people():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, first_name, last_name FROM person')
        people = cursor.fetchall()
        cursor.close()
        conn.close()
        return people

    @staticmethod
    def search_users(username="", role="", active=""):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT users.id, users.username, users.active, users.person_id, person.first_name, person.last_name,
                   GROUP_CONCAT(roles.name) AS roles
            FROM users
            JOIN person ON users.person_id = person.id
            LEFT JOIN user_roles ON users.id = user_roles.user_id
            LEFT JOIN roles ON user_roles.role_id = roles.id
            WHERE 1=1
        '''
        params = []
        if username:
            query += " AND users.username LIKE %s"
            params.append(f"%{username}%")
        if role:
            query += " AND roles.name = %s"
            params.append(role)
        if active != "":
            query += " AND users.active = %s"
            params.append(bool(int(active)))
        query += " GROUP BY users.id"
        cursor.execute(query, params)
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users 

    @staticmethod
    def get_user_by_person_id(person_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE person_id = %s', (person_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def is_username_taken(username):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = %s', (username,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count > 0 

    @staticmethod
    def update_user_password(user_id, new_password):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET password = %s WHERE id = %s', (new_password, user_id))
        conn.commit()
        cursor.close()
        conn.close() 