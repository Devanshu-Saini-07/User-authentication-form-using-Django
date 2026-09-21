# Django User Authentication App

A reusable, beginner-friendly Django application for handling user authentication (registration, login, logout, password reset, change password, profile).

## Features

- User Registration (Username, Email, Password)
- Login / Logout
- Dashboard (Protected)
- Profile Page (Protected)
- Change Password (Authenticated users only)
- Complete Password Reset Flow (via Email)

## Installation

```bash
# Clone the repository
git clone <repository_url>
cd <repository_name>

# Setup virtual environment
python -m venv venv
venv\Scripts\activate

# Install Django
pip install django

# Run migrations
python manage.py makemigrations auth_app
python manage.py migrate

# Run server
python manage.py runserver
```

## How to reuse this app

Include `auth_app` in your Django project `INSTALLED_APPS` and include its URLs in your root `urls.py`:

```python
path("auth/", include("auth_app.urls"))
```

Ensure `LOGIN_URL`, `LOGIN_REDIRECT_URL`, and `LOGOUT_REDIRECT_URL` are configured in your `settings.py`.

## Password Reset Testing

By default, this project uses the Django console email backend. Password reset emails will appear in your terminal. Copy the reset URL and paste it into your browser to test.

## Production Email

For production, configure SMTP settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
EMAIL_USE_TLS = True
```
