FROM python:3.9.7

RUN mkdir -p /opt/application/ubademy-back-py

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml /opt/application/ubademy-back-py
COPY alembic.ini /opt/application/ubademy-back-py
ADD alembic /opt/application/ubademy-back-py/alembic
COPY run.sh /opt/application/ubademy-back-py

WORKDIR /opt/application/ubademy-back-py
COPY app .

RUN apt-get update
RUN pip install poetry
RUN poetry install
ENV DATABASE_HOST postgres-db
EXPOSE 8080

ENTRYPOINT ["poetry", "run", "./run.sh"]
