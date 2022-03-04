FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
RUN poetry add gunicorn

EXPOSE $PORT
CMD gunicorn -b 0.0.0.0:$PORT discuss_api.wsgi:application