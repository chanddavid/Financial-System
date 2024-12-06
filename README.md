# Financial Management API

This is a Financial Management API built with Django and Django REST Framework, providing endpoints for managing income, expenses, loans, and generating financial trends and summaries.

---

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Project](#running-the-project)
5. [API Documentation](#api-documentation)
6. [Project Structure](#project-structure)

---

## Requirements

- **Python Version**: `3.10.12`
- **Django Version**: `5.x` or above
- **DRF Version**: `3.x` or above
- Other dependencies are listed in `requirements.txt`.

---

## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/chanddavid/Financial-System.git
    ```

2. **Create a Virtual Environment**:
    ```bash
    python3 -m venv env
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run Development Server**:
    ```bash
    python manage.py runserver
    ```

---

## Configuration

### `.env` File

- Create a `.env` file in the root directory of the project.
- Add the following credentials to configure the project:
    ```env
    SECRET_KEY=your_django_secret_key
    DEBUG=True
    DATABASE_URL=your_database_url
    JWT_SECRET=your_jwt_secret_key
    ```

- Ensure `.env` file is added to `.gitignore` to avoid exposing sensitive data.

---

## Running the Project

1. **Activate the Virtual Environment**:
    ```bash
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

2. **Run Development Server**:
    ```bash
    python manage.py runserver
    ```

3. Open the server in your browser or API client:
    ```
    http://127.0.0.1:8000/admin/
    ```

---

## API Documentation

- **Swagger**: API documentation is available at:
    ```
    http://127.0.0.1:8000/swagger/
    ```
- **ReDoc**: Alternative documentation can be found at:
    ```
    http://127.0.0.1:8000/redoc/
    ```

---


