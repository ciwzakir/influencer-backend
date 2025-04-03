## Deploy on pythonanywhere

pROJECT INFO:

- SuperUser : superone
- Email : z@gmail.com
- PASSWORD : 1234

Activate virtual env:

- python manage.py makemigrations contribution
- python manage.py makemigrations basics
- python manage.py makemigrations userprofile
- python manage.py migrate basics
- python manage.py migrate contribution

- source projenv/Scripts/activate
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver
- python manage.py createsuperuser

- python manage.py makemigrations contribution, basics, fundstates, investments, userprofile
- python manage.py migrate contribution, basics, fundstates, investments, userprofile
- python manage.py makemigrations userprofile
