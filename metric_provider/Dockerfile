FROM python:alpine

WORKDIR /car

ADD . .

RUN pip install -U pip && pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]