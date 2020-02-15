# dresden-rallye-backend
Backend for storing data, intensive computing, routing

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Geospatial libraries:
- GEOS
- PROJ.4
- GDAL

Database:
- PostgreSQL 12
- PostGIS

### Installing

Create an empty file named .env in the root directory and configure environmental variables. Sample .env file content:
```
DEBUG=True
SECRET_KEY=****************

DB_USER=django
DB_PASSWORD=********
DB_HOST=127.0.0.1
DB_PORT=5432
```

Create a virtual Python environment and install required modules:
```shell
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Create project database and connect to PostgreSQL server using terminal:
```shell
$ createdb ddrallye
$ psql ddrallye
```

Install the PostGIS extension:
```SQL
CREATE EXTENSION postgis;
```

Create a database user for the Django application and grant them access to the database:
```SQL
CREATE USER django PASSWORD 'password';
GRANT CONNECT ON DATABASE ddrallye TO django;
GRANT USAGE ON SCHEMA public TO django;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO django;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO django;
```

Migrate the Django data model to the database:
```shell
$ python manage.py makemigrations
$ python manage.py migrate
```

Create an admin account:
```shell
$ python manage.py createsuperuser
```

### Startup

Start the Django development server:
```shell
$ python manage.py runserver
```

## Deployment

TODO