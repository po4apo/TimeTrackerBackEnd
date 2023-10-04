#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for Postgres"
    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "Postgers started"
fi

python -V
python manage.py makemigrations TimeTrackerBackEnd
python manage.py migrate


exec "$@"
