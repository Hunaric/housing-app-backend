To authorize any user to edit file inside the project: `sudo chown -R $USER:$USER ~/Documents/Projects/Python`
Command to make superuser with docker compose: `docker compose exec web python manage.py createsuperuser`
Command to run docker server: `$docker compose up --build` and to do the same in the background, change '--build' by '-d'