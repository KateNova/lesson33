FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY todolist todolist
WORKDIR /code/todolist
CMD python3 manage.py runserver localhost:8000