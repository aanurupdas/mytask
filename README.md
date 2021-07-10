# Todo API
Similar project based on `python3.8` , `Django3.1` , `Django-REST-Framework3.12`

## Features:
1. Register API with first_name,last_name,email and activation link send to that email. API Endpoint-
- (POST) - `http://127.0.0.1:8000/api/signup`
- Example Activation link: `https://example.in/verify-user/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI1OTI1OTgxLCJqdGkiOiJmZTJmMDg5NGNjZWE0YzY4YmNhNDdjZTg2NTNjYTc5OSIsInVzZXJfaWQiOjZ9.r06RM2CJHBhZj_ED0YPgGtWdxt6ufufCFklBw0dG_cg/`
- Activation link has expiry time of 15 minutes(can be changed)
- This token is JWT encoded.

2. Activate Email API, set Password. API Endpoint- 
- (PUT) - `http://127.0.0.1:8000/api/verify-user/{token}/`
- Example {token}: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI1OTI1OTgxLCJqdGkiOiJmZTJmMDg5NGNjZWE0YzY4YmNhNDdjZTg2NTNjYTc5OSIsInVzZXJfaWQiOjZ9.r06RM2CJHBhZj_ED0YPgGtWdxt6ufufCFklBw0dG_cg
- Copy and put this {token} in above endpoint.
- Activation link has expiry time of 15 minutes(can be changed)
- This token is JWT encoded.

3. Resend verification email API with email and activation link send to that email. API Endpoint- 
- (POST) - `http://127.0.0.1:8000/api/resend`

4. User Signin/Login API and in response gives JWT Tokens encoded. API Endpoint-
- (POST) - `http://127.0.0.1:8000/api/signin` 

NOTE: APIs checked with POSTMAN software.

## Installation:
On Local Server, Install via pip: 
```bash
pip install -r requirements.txt
```

## Create Table:
On Local Server, Run command in terminal:
```bash
python manage.py migrate
```

## Create SuperUser:
On Local Server, Run command in terminal:
```bash
python manage.py createsuperuser
```

## Start Server
On Local Server,Run command in terminal:
```bash
python manage.py runserver
```
Open Local Server `http://127.0.0.1:8000` in your browser.

## Access Django Admin Panel:
To access Django Admin Panel `http://127.0.0.1:8000/admin` , Use Credentials: 
- Email: admin@admin.in 
- Password: admin
