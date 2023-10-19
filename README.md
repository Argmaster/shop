# Django web application

## Startup

This application was designed to work with `podman` and `podman-compose` (or `docker`
and `docker-compose`).

On linux (Debian, Ubuntu) one may install those with:

```bash
sudo apt install podman && sudo apt install podman-compose
```

To run development version of application setup, prepare configuration file, `.env.dev`
in repository root:

```toml
# Django config.
DEBUG=1
SECRET_KEY=some secret key
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1] 192.168.1.3
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=django_shop_db_dev
SQL_USER=admin
SQL_PASSWORD=example password
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
# Postgres config.
POSTGRES_USER=admin
POSTGRES_PASSWORD=example password
POSTGRES_DB=django_shop_db_dev
```

Now you will need to create `requirements.txt` file. You will need `poetry` to do this.
You can install it from PyPI with:

```bash
pip install poetry
```

After installing poetry, you can use it to dump web application requirements with
following:

```bash
poetry shell && poetry install && poetry export > "app/requirements.txt"
```

Afterwards you can start application with `podman-compose`:

```bash
podman-compose -f ./docker-compose.yml up --detach
```

Now to check container status you can use following:

```bash
podman-compose ps
```

It should print something like this:

```
['podman', '--version', '']
using podman version: 4.3.1
podman ps -a --filter label=io.podman.compose.project=shop
CONTAINER ID  IMAGE                                     COMMAND               CREATED             STATUS                 PORTS                   NAMES
9674f8940726  docker.io/library/postgres:15.4-bookworm  postgres              About a minute ago  Up About a minute ago                          shop_db_1
58a3fa7eb149  localhost/shop_web:latest                 python manage.py ...  About a minute ago  Up About a minute ago  0.0.0.0:8000->8000/tcp  shop_web_1
exit code: 0
```

If you are starting this application for the first time, you will have to first set up
the database with:

```bash
podman-compose exec web python manage.py migrate
```

Afterwards you will be able to create administrator account:

```bash
podman-compose exec web python manage.py createsuperuser
```

This command will prompt you for username and password for administrator. Then you will
be able to log into administrator page on
[`http://127.0.0.1:8000/admin/`](http://127.0.0.1:8000/admin/)

To stop running containers use:

```
podman-compose down
```
