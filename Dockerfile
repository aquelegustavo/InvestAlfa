FROM ghcr.io/sghufsc/docker-python-poetry:latest

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

RUN poetry shell

CMD gunicorn investalfa.wsgi:application --bind 0.0.0.0:$PORT