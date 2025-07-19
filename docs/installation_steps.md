# Installation Steps for Student Management System (SMS)

This guide will help you set up and run the Student Management System (SMS) web application on your local machine.

---

## 1. Install Python

- Download and install Python 3.10 or newer from the [official Python website](https://www.python.org/downloads/).
- During installation, **ensure you check the box "Add Python to PATH"**.
- Verify installation:

```sh
python --version
```

---

## 2. Create a Virtual Environment

- Open a terminal/command prompt in the project root directory (`sms`).
- Run the following command to create a virtual environment named `.venv`:

```sh
python -m venv .venv
```

- Activate the virtual environment:
  - **Windows:**
    ```sh
    .venv\Scripts\activate
    ```
  - **macOS/Linux:**
    ```sh
    source .venv/bin/activate
    ```

---

## 3. Install Python Dependencies

- With the virtual environment activated, install all required packages:

```sh
pip install -r requirements.txt
```

---

## 4. Create the MySQL Database

- Install MySQL Server if not already installed. [Download MySQL](https://dev.mysql.com/downloads/mysql/)
- Start the MySQL service.
- Log in to MySQL as root or a user with privileges:

```sh
mysql -u root -p
```

- Run the schema script to create the database and tables:

```sql
SOURCE database/schema.sql;
```

- (Optional) You can also run any additional SQL scripts in the `database/` folder as needed.

- **Set up a MySQL user and password** (if not already done) and update the environment variables in your system or a `.env` file in the project root:

```
DB_HOST=localhost
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=student_mgmt
WEB_SESSION_SECRET_KEY=your_secret_key
WEB_SESSION_TIMEOUT=3600
```

---

## 5. Run the Application Using Uvicorn

- Make sure your virtual environment is activated.
- In the project root, run:

```sh
uvicorn app.main:app --reload
```

- The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 6. Default Users, Roles, and Passwords

After running the schema, the following default users and roles are typically available (if inserted by your SQL scripts):

| Username   | Password   | Role           |
|------------|------------|----------------|
| admin      | admin123   | Administrator  |
| faculty1   | faculty123 | Faculty        |
| student1   | student123 | Student        |

- **Note:** If your `schema.sql` or setup scripts do not insert these users, you may need to add them manually using SQL or the application's user management screens.
- Change default passwords after first login for security.

---

**You are now ready to use the Student Management System!** 