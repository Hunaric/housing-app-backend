#!/bin/sh

if [ "$DATABASE" = "postgres" ] 
then
    echo "Check if database is running..."

    while ! nc -z $SQL_HOST $SQL_PORT; do 
        sleep 0.1
    done

    echo "The database is up and running :-D"
fi

python manage.py makemigrations || echo "Migrations failed"
python manage.py migrate || echo "Migration application failed"

# 🔥 Ajout de cette ligne pour lancer Django sur le bon port
exec python manage.py runserver 0.0.0.0:${PORT:-8000}
