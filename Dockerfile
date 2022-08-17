FROM ghcr.io/sghufsc/docker-python-poetry:latest

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

RUN poetry shell

CMD [ "python3", "manage.py" , "runserver"]