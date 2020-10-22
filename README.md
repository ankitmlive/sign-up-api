# django-rest-api for react-signup

This is demo api created for react-signup example.

## Dependencies

Python3 and virtualenv should be installed in development machine

# Installation

git clone https://github.com/ankitmlive/sign-up-api.git
cd sign-up-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver

# Endpoint (POST)

http://localhost:8000/api/v1/accounts/register/

# payload (with a url encoded post)

firstname 
lastname
organization
phone
registration
password

## Warning :

This app is only for demonstration, No validation or error-handling implemented yet.
    






