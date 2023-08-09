#!/bin/bash
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate
sudo chown -R "$USER":"$USER" app
