# 📄 PDF Utility Tool

A lightweight, powerful, and user-friendly web application built with **Django** and **PyPDF2** for everyday PDF manipulation tasks, including merging multiple documents and extracting custom page ranges.

[![CI](https://github.com/Abhishek-Developer22/PDF-utility-Tool/actions/workflows/ci.yml/badge.svg)](https://github.com/Abhishek-Developer22/PDF-utility-Tool/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-darkgreen.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Features

- **📑 Merge PDFs:** Combine two or more PDF files into a single document in just one click.
- **✂️ Extract Pages:** Extract specific pages or custom page ranges (e.g., `1,3,5` or `2-8` or `1,4,6-10`) into a new PDF.
- **🛡️ Robust Form Validation:**
  - Enforces minimum file requirements (e.g., requires at least 2 files for merging).
  - Validates `.pdf` file types and checks for corrupted inputs.
  - Page range syntax validation using regular expressions.
- **📊 Real-time Log Viewer:** Integrated logging system with an accessible web viewer (`/logs/`) to track operations and troubleshoot errors.
- **🎨 Clean & Responsive UI:** Styled with modern CSS/Bootstrap for a seamless experience on desktop and mobile devices.
- **⚡ Production Ready:** Pre-configured with **WhiteNoise** for serving static files, **Gunicorn** WSGI HTTP server, and automated **GitHub Actions CI**.

---

## 🛠️ Tech Stack

- **Backend Framework:** [Django 5.x](https://www.djangoproject.com/)
- **Language:** [Python 3.11+](https://www.python.org/)
- **PDF Engine:** [PyPDF2](https://pypi.org/project/PyPDF2/)
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **WSGI Server:** [Gunicorn](https://gunicorn.org/)
- **Static Assets:** [WhiteNoise](http://whitenoise.evans.io/)
- **Testing & CI:** Pytest, Pytest-Django, Ruff, GitHub Actions

---

## 📂 Project Structure

```text
PDF Utilty Tool/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow (linting & testing)
├── pdf_tool/                  # Core application
│   ├── templates/pdf_tool/    # HTML templates (base, home, merge, extract)
│   ├── forms.py               # Form classes & validation logic
│   ├── services.py            # PDF processing core logic (PyPDF2)
│   ├── tests.py               # Automated unit tests
│   ├── urls.py                # App routing
│   └── views.py               # Request handlers
├── pdf_utility/               # Project configuration
│   ├── settings.py            # Django configuration
│   ├── urls.py                # Root URL routing
│   └── wsgi.py                # WSGI entry point
├── build.sh                   # Build script for cloud deployment (Render)
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── .gitignore                 # Ignored files (venv, logs, etc.)
```

---

## 💻 Local Installation & Setup

### Prerequisites
Make sure you have **Python 3.11+** and **Git** installed on your system.

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Abhishek-Developer22/PDF-utility-Tool.git
   cd PDF-utility-Tool
   ```

2. **Create and activate a virtual environment:**
   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. Open your browser and navigate to:
   ```text
   http://127.0.0.1:8000/
   ```

---

## 🧪 Running Tests & Linting

Run automated tests using `pytest`:
```bash
pytest
```

Check code formatting and linting using `ruff`:
```bash
ruff check .
```

---

## 🌐 Free Cloud Deployment (Render.com)

This repository is ready to be deployed on **Render.com** (100% Free):

1. Go to [Render Dashboard](https://dashboard.render.com/) and click **New + > Web Service**.
2. Connect your GitHub repository (`PDF-utility-Tool`).
3. Fill in the deployment settings:
   - **Environment:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn pdf_utility.wsgi:application`
   - **Plan:** `Free`
4. Click **Deploy Web Service**.

---

## 👤 Author

- **Abhishek** - [GitHub Profile](https://github.com/Abhishek-Developer22)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
