FROM python:3.9.7

RUN mkdir -p /opt/application/ubademy-back-py
COPY pyproject.toml /opt/application/ubademy-back-py
COPY run.sh /opt/application/ubademy-back-py
COPY prestart.sh /opt/application/ubademy-back-py
WORKDIR /opt/application/ubademy-back-py

RUN apt-get update
RUN pip install poetry
RUN poetry install
ENV DATABASE_HOST postgres-db
EXPOSE 8080
RUN poetry run ./prestart.sh

ENTRYPOINT ["poetry", "run", "./run.sh"]
