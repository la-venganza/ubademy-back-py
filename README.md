[![Build Status](https://app.travis-ci.com/la-venganza/ubademy-back-py.svg?branch=develop)](https://app.travis-ci.com/la-venganza/ubademy-back-py)

[![Coverage Status](https://coveralls.io/repos/github/la-venganza/ubademy-back-py/badge.svg?branch=develop)](https://coveralls.io/github/la-venganza/ubademy-back-py?branch=develop)

# ubademy-back-py
Taller 2 - 2c 2021 - Backend python repository


## Alembic - Database changes
When a change to the database is made, run following command to capture the change
```bash
alembic revision --autogenerate -m "Description of change"
```

If command doesn't work, try using prefix: PYTHONPATH=. as 
```bash
PYTHONPATH=. alembic revision --autogenerate -m "Description of change"
```

Run to make sure database is up to date
```bash
PYTHONPATH=. alembic upgrade head
```

If you want to go back to a previous version
```bash
PYTHONPATH=. alembic downgrade version
```

Or you just want to downgrade before last version
```bash
PYTHONPATH=. alembic downgrade -1
```

## How to run 

```bash
docker-compose build
docker-compose up -d
```

## Swagger UI docs

```bash
http://localhost:8080/docs
```

## ReDoc docs

```bash
http://localhost:8080/redoc
```


## How to browse

```bash
http://localhost:8080/api/v1/courses
http://localhost:8080/api/v1/courses/1
```

## How to run tests

```bash
py.test
```
