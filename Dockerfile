FROM python:3.11.1
LABEL authors="main"

ENV PYTHONUNBUFFERED 1

COPY . /backend/
WORKDIR /backend



RUN pip install -r requirements.txt

CMD python3 manage.py runserver
# CMD ["%%CMD%%"]