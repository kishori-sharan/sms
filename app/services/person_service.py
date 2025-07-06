from app.services.db_service import DBService

class PersonService:
    @staticmethod
    def get_person(person_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM person WHERE id=%s", (person_id,))
        person = cursor.fetchone()
        cursor.close()
        conn.close()
        return person

    @staticmethod
    def get_addresses(person_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM addresses WHERE person_id=%s", (person_id,))
        addresses = cursor.fetchall()
        cursor.close()
        conn.close()
        return addresses

    @staticmethod
    def get_contacts(person_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM contact_info WHERE person_id=%s",
            (person_id,)
        )
        contacts = cursor.fetchall()
        cursor.close()
        conn.close()
        return contacts

    @staticmethod
    def get_roles(person_id):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT roles.name FROM users
            JOIN user_roles ON users.id = user_roles.user_id
            JOIN roles ON user_roles.role_id = roles.id
            WHERE users.person_id=%s
        """, (person_id,))
        roles = [row["name"] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return roles

    @staticmethod
    def update_person(person_id, first_name, last_name, birth_date, gender):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE person SET first_name=%s, last_name=%s, birth_date=%s, gender=%s WHERE id=%s",
            (first_name, last_name, birth_date, gender, person_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_person(person_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM person WHERE id=%s", (person_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def list_persons():
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM person")
        persons = cursor.fetchall()
        cursor.close()
        conn.close()
        return persons

    @staticmethod
    def add_person(first_name, last_name, birth_date, gender):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO person (first_name, last_name, birth_date, gender) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, birth_date, gender),
        )
        person_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return person_id

    @staticmethod
    def add_address(person_id, address_type, address_line1, address_line2, city, state, postal_code, country):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO addresses (person_id, address_type, address_line1, address_line2, city, state, postal_code, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (person_id, address_type, address_line1, address_line2, city, state, postal_code, country),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def add_contact(person_id, contact_type, contact_value):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contact_info (person_id, contact_type, contact_value) VALUES (%s, %s, %s)",
            (person_id, contact_type, contact_value),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_address(address_id, address_type, address_line1, address_line2, city, state, postal_code, country):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE addresses SET address_type=%s, address_line1=%s, address_line2=%s, city=%s, state=%s, postal_code=%s, country=%s WHERE id=%s",
            (address_type, address_line1, address_line2, city, state, postal_code, country, address_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_address(address_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM addresses WHERE id=%s", (address_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_contact(contact_id, contact_type, contact_value):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE contact_info SET contact_type=%s, contact_value=%s WHERE id=%s",
            (contact_type, contact_value, contact_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_contact(contact_id):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contact_info WHERE id=%s", (contact_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def count_persons(first_name, last_name, birth_date, gender, role):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT COUNT(*)
            FROM person
            LEFT JOIN users ON users.person_id = person.id
            LEFT JOIN user_roles ON users.id = user_roles.user_id
            LEFT JOIN roles ON user_roles.role_id = roles.id
            WHERE 1=1
        """
        params = []
        if first_name:
            query += " AND person.first_name LIKE %s"
            params.append(f"%{first_name}%")
        if last_name:
            query += " AND person.last_name LIKE %s"
            params.append(f"%{last_name}%")
        if birth_date:
            query += " AND person.birth_date = %s"
            params.append(birth_date)
        if gender:
            query += " AND person.gender = %s"
            params.append(gender)
        if role:
            query += " AND roles.name = %s"
            params.append(role)
        cursor.execute(query, params)
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count

    @staticmethod
    def search_persons(first_name, last_name, birth_date, gender, role, offset, limit, sort_by="first_name", sort_order="asc"):
        conn = DBService.get_connection()
        cursor = conn.cursor(dictionary=True)
        # Whitelist allowed columns to prevent SQL injection
        allowed_sort_columns = {
            "id": "person.id",
            "first_name": "person.first_name",
            "last_name": "person.last_name",
            "birth_date": "person.birth_date",
            "gender": "person.gender",
            "role": "roles.name"
        }
        sort_column = allowed_sort_columns.get(sort_by, "person.first_name")
        sort_order = "desc" if sort_order == "desc" else "asc"
        query = f"""
            SELECT person.id, person.first_name, person.last_name, person.birth_date, person.gender, roles.name as role
            FROM person
            LEFT JOIN users ON users.person_id = person.id
            LEFT JOIN user_roles ON users.id = user_roles.user_id
            LEFT JOIN roles ON user_roles.role_id = roles.id
            WHERE 1=1
        """
        params = []
        if first_name:
            query += " AND person.first_name LIKE %s"
            params.append(f"%{first_name}%")
        if last_name:
            query += " AND person.last_name LIKE %s"
            params.append(f"%{last_name}%")
        if birth_date:
            query += " AND person.birth_date = %s"
            params.append(birth_date)
        if gender:
            query += " AND person.gender = %s"
            params.append(gender)
        if role:
            query += " AND roles.name = %s"
            params.append(role)
        query += f" ORDER BY {sort_column} {sort_order} LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        cursor.execute(query, params)
        persons = cursor.fetchall()
        cursor.close()
        conn.close()
        return persons