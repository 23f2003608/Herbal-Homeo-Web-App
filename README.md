# Herbal Homeo – Clinic Management System

A Flask-based web application built for **Herbal Homeo**, a local homeopathic clinic owned and managed by **Dr. Shikhar Sharma**. The system helps manage patients, expenses, notices, and clinic operations through a clean, centralized dashboard.

---

## 🚀 Features

* **User Authentication:** Secure Login and Logout functionality.
* **Patient Management:** Add, update, and track patient records easily.
* **Expense Tracking:** Monitor clinic expenditures.
* **Notices & Updates:** Post important clinic updates on the dashboard.
* **Dashboard Overview:** Get a quick glance at clinic stats.
* **PDF Support:** Generation support for reports/prescriptions.
* **Responsive UI:** Clean interface built with modern templates and assets.

---

## 🛠 Tech Stack

* **Backend:** Python (Flask)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite (SQLAlchemy ORM)
* **Auth:** Flask-Login

---

## 📂 Project Structure

```text
app/
├── auth/          # Authentication logic
├── dashboard/     # Main dashboard views
├── expenses/      # Expense management module
├── notices/       # Notice board module
├── patients/      # Patient records module
├── static/        # CSS, JS, and Uploaded files
└── templates/     # HTML templates
instance/          # Database instance
migrations/        # Database migrations
requirements.txt   # Project dependencies
run.py             # Application entry point

```

---

## ⚙️ Setup Instructions (Local)

### 1. Clone the repository

```bash
git clone [https://github.com/23f2003608/herbal_homeo.git](https://github.com/your-username/herbal_homeo.git)
cd herbal_homeo

```

### 2. Create a virtual environment

```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

```

### 3. Install dependencies

```bash
pip install -r requirements.txt

```

### 4. Environment variables

Create a `.env` file in the root directory:

```env
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///app.db

```

### 5. Run the Application

```bash
flask run
# OR
python run.py

```

App will be live at: **http://127.0.0.1:3000**

---

## 🚫 Ignored Files

The following files are excluded from version control for security and cleanliness:

* `venv/`
* `.env`
* `instance/`
* `__pycache__/`
* `app/static/uploads/`

---

## 🌐 Deployment Notes

1. Install dependencies via `requirements.txt`.
2. Set production environment variables on the server.
3. Configure a production WSGI server like **Gunicorn**.
4. Run database migrations before the first use.

---

## 👨‍⚕️Current Client

**Herbal Homeo Clinic** *Owned & managed by Dr. Shikhar Sharma*

---

## 📄 License

This project is developed for a private clinic and is not intended for public redistribution without explicit permission.

```

