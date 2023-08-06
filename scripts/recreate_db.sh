#!/bin/bash
sudo docker-compose down
sudo rm -rf postgres_data
poe manage makemigrations
sudo docker-compose up -d --build
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser --username root --email "root@root.com"
