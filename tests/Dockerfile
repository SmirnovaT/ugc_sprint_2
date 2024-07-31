FROM python:3.11-slim

WORKDIR /tests/

COPY poetry.lock pyproject.toml /tests/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE 0
ENV POETRY_NO_INTERACTION 1


RUN  pip install --upgrade pip && pip install poetry==1.8.3

RUN poetry config virtualenvs.create false && poetry install

COPY . .

RUN chmod u+x commands.sh

CMD ["/bin/sh", "/tests/commands.sh"]