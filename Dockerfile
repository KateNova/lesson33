FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY todolist todolist
WORKDIR /code/todolist
CMD gunicorn todolost.wsgi --workers 3 --bind=localhost:8000