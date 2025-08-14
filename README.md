# 📚 Akshardham E-Library Management

**Live Demo:** [View Project on Render](https://akshardham-library.onrender.com)

A complete **Flask-based e-library management system** that allows administrators to manage books and sections, handle user requests, and view library statistics.  
Users can browse books, request to borrow them, submit feedback, and view their borrowed history.  

---

## 🚀 Features

### 👨‍💼 Admin
- Secure login for administrators.
- Manage sections (add, update, delete).
- Manage books (add, update, delete).
- Approve or reject book borrow requests.
- View user details and revoke issued books.
- Library statistics visualization with **Matplotlib**.

### 👤 User
- Secure login and registration.
- Browse books by section, title, or author.
- Request books (with limit on active borrowings).
- View issued books and return them.
- Submit feedback on books.

---

## 🛠 Tech Stack

**Backend:** Python, Flask, SQLAlchemy  
**Database:** SQLite  
**Frontend:** HTML5, CSS3, Jinja2 Templates  
**Libraries:** Matplotlib, Collections, Datetime  

---

## 📂 Project Structure

project/
│
├── app.py # Flask app factory and initialization
├── models.py # Database models
├── routes.py # All application routes
├── static/ # CSS, JS, images
├── templates/ # HTML templates
├── instance/ # SQLite database file
├── venv/ # Virtual environment (excluded from Git)
└── requirements.txt # Project dependencies

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/akshardham-e-library-management.git
cd akshardham-e-library-management

2️⃣ Create a virtual environment
python -m venv venv

3️⃣ Activate the environment

Windows (PowerShell):

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

4️⃣ Install dependencies
pip install -r requirements.txt

5️⃣ Run the application
python app.py


The app will start on:

http://127.0.0.1:5000/

📊 Admin Statistics

The system generates a Book Request Status bar chart showing:

Pending requests

Approved requests

Rejected requests

The chart is automatically saved in static/ and displayed in the admin dashboard.
