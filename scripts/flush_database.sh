#!/bin/bash
sudo docker-compose exec web python manage.py flush --no-input
sudo docker-compose exec web python manage.py migrate
