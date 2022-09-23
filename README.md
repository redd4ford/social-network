# social-network
This is the test task for StarNavi.

This project was developed with: Python 3.8, Django 4.0.5, PostgreSQL 14

Uses libraries: Django Rest Framework, DRF-Spectacular, DRF-Nested-Routers, SimpleJWT, DRF-YASG & Swagger, Django-Environ, Django-Filter, Django-Injector.

***
# Setup

* Create venv: `python -m venv /path/to/venv`
* Activate venv:
  * Linux/MacOS: `source venv/bin/activate`
  * Windows: `venv\Scripts\activate`
* Install requirements: `pip install -r requirements.txt`
* Create a PostgreSQL database 
* Create `socialnetwork/.env` file based on `.env.example`
  * To generate `SECRET_KEY`, use: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
* Run migrations: `python manage.py migrate`
* Start the server: `python manage.py runserver`
* Find the OpenAPI here: [http://127.0.0.1:8000/schema/swagger-ui/#/](http://127.0.0.1:8000/schema/swagger-ui/#/)

***
# Implemented

* Models: User, Post, Like
* Endpoints: Post CRUD, Post like/unlike, User sign up/sign in/sign out/refresh (JWT-based), user activity, likes analytics (by post, by user, by dates (date_from, date_to))