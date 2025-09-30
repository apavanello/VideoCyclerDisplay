#!/bin/bash

#get random  django secret key function and return the key from openssh
    function generate_secret_key() {
        local SECRET_KEY
        SECRET_KEY=$(openssl rand -base64 48 | tr -d /=+ | cut -c1-50)
        echo "$SECRET_KEY"
    }

#if .env dont exist the create it
if [ ! -f .env ]; then
    touch .env
    echo "Created .env file"
    cat << EOF > .env
# Django settings
SECRET_KEY=$(generate_secret_key)
DEBUG=True
ALLOWED_HOSTS=*
EOF
fi

#start docker compose
docker-compose build

#run migrations
docker-compose run --rm web python manage.py migrate
#collect static files
docker-compose run --rm web python manage.py collectstatic --noinput
# Create superuser if first run
if [ ! -f .first_run ]; then
    docker-compose run --rm web python manage.py createsuperuser
    touch .first_run
fi
#start the server
docker-compose up -d