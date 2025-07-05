# Student Management System (SMS)

## 1. Set Up Python Environment

> ✅ **Option A: If you're using PyCharm**

* PyCharm automatically creates a virtual environment in a folder named `.venv` in your project root.
* You can install dependencies from **Terminal** or PyCharm's **Python Packages tool window**.

```bash
# Inside PyCharm Terminal
pip install -r requirements.txt
```

> ✅ **Option B: If you're using terminal (outside PyCharm)**

1. Create a virtual environment in the `.venv` folder:

   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:

   * **Linux/macOS**:

     ```bash
     source .venv/bin/activate
     ```
   * **Windows (Command Prompt)**:

     ```cmd
     .venv\Scripts\activate
     ```
   * **Windows (PowerShell)**:

     ```powershell
     .venv\Scripts\Activate.ps1
     ```

3. Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

---

## 2. Set Up Database

Run the following command in a terminal to set up the database and tables:

```bash
mysql -u root -p < database/schema.sql
```

---

## 3. Configure Database Credentials

Create a `.env` file in your project root folder with this content:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=mySMS#1942
DB_NAME=student_mgmt
WEB_SESSION_SECRET_KEY=mySecret^1942
WEB_SESSION_TIMEOUT=3600
MAX_SEARCH_RESULTS=5000
```

Replace `your_db_username` and `your_db_password` with your actual MySQL credentials.

---

Here’s the updated **README.md** section to include **both ways** of running your FastAPI application (via `uvicorn` and directly using `python main.py`):

---

## 4. Run the Application

You have **two options** to run the FastAPI app:

### ✅ Option A: Preferred Method (using `uvicorn`)

From your project root directory (`sms/`), run:

```bash
 uvicorn app.main:app --reload --log-level debug
```

Then open your browser and navigate to:

```
http://127.0.0.1:8000
```

### ✅ Option B: Run with `python` (for convenience)

If you prefer running the app directly with Python, add the following block at the **bottom of your `app/main.py`**:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
```

Then run from your `sms/` directory:

```bash
python app/main.py
```

> ⚠️ Note: Use Option A (`uvicorn`) as the recommended method in most development and deployment environments.

---



## 5. Sample Credentials for Login

| Role          | Username | Password    | Role in Dropdown  |
| ------------- | -------- | ----------- | ----------------- |
| Administrator | admin    | password123 | Administrator     |
| Student       | student  | password123 | Student (default) |
| Faculty       | faculty  | password123 | Faculty           |

---

## 6. Packaging Your Project

* Ensure the project directory follows the structure described earlier.
* Do **not** include `.env` in the ZIP file if it contains real credentials.
* Zip the entire `sms/` folder.
* The zipped project is now ready for submission or sharing.

---

