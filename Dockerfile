FROM python:3.11.1
LABEL authors="main"

ENTRYPOINT ["top", "-b"]

ENV PYTHONUNBUFFERED 1

WORKDIR .

COPY . .

RUN ls .


RUN pip install -r requirements.txt

EXPOSE 8080

CMD python3 manage.py runserver 10.128.0.6:8000
# CMD ["%%CMD%%"]