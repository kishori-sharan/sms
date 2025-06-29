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
        conn.commit()
        cursor.close()
        conn.close()