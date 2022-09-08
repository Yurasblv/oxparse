-[x] FINISHED 

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

# Flask application for scrapping data using selenuim and chromedriver.

### First of all clone this repository and set up .env file with following vars:
```
-POSTGRES_USER
-POSTGRES_PASSWORD
-POSTGRES_DB
-POSTGRES_PORT
-POSTGRES_HOST
-SECRET_KEY
-SQLALCHEMY_DATABASE_URI
```

All commands in Makefile:

    to start scrapping enter : 

            make start

    to stop scrapping enter : 

            make stop

    clean docker system : 

            make clean

*How it works*

``Database and app work each in personal container , while database ready for connection ,flask app start running.
Due to dynamical updating scrapping resourse , app will grab info till it not find information on the page.To stop working containers just use CTRL+C``

