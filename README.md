# django-user-authentication

A beginner-friendly Django user authentication project built with Django's built-in authentication system. It demonstrates signup, login, logout, profile management, password changes, password resets, protected routes, Django messages, form validation, sessions, CSRF protection, and responsive Bootstrap 5 templates.

## Features

- User signup with email validation and duplicate email protection
- User login with success and error messaging
- Secure logout flow
- Protected dashboard using `@login_required`
- User profile page
- Edit profile with duplicate username and email validation
- Password change while keeping the user logged in
- Full password reset flow using Django's built-in views
- Redirect authenticated users away from login and signup pages
- Responsive Bootstrap 5 user interface with custom CSS and JavaScript

## Technologies Used

- Python
- Django
- Bootstrap 5
- SQLite
- HTML templates
- CSS
- JavaScript

## Project Structure

```text
django-user-authentication/
├── accounts/
│   ├── migrations/
│   ├── templates/accounts/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   ├── css/style.css
│   ├── images/
│   └── js/script.js
├── templates/
│   ├── base.html
│   └── dashboard.html
├── .env.example
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

## Installation Instructions

1. Clone the repository:

```bash
git clone https://github.com/Devanshu-Saini-07/django-user-authentication.git
cd django-user-authentication
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

```bash
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create your environment file:

```bash
copy .env.example .env
```

6. Apply migrations:

```bash
python manage.py migrate
```

7. Run the development server:

```bash
python manage.py runserver
```

## Password Reset in Development

This project uses the following development email backend:

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

That means password reset emails are printed directly in the terminal instead of being sent to a real inbox. When you submit the password reset form locally, copy the reset link from the terminal output and open it in your browser.

## Screenshots

- Home dashboard screenshot: add screenshot here
- Login page screenshot: add screenshot here
- Signup page screenshot: add screenshot here
- Profile page screenshot: add screenshot here

## Future Improvements

- Add user avatar uploads
- Add email verification after signup
- Add automated tests for forms and views
- Add production deployment instructions

## Author

Devanshu Saini  
GitHub: [Devanshu-Saini-07](https://github.com/Devanshu-Saini-07)
