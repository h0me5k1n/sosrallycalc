# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
EXPOSE 3000

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt
ADD static static
ADD templates templates
COPY templates .
COPY app.py .
COPY check_format.py .
COPY format.py .
COPY keep_alive.py .

SHELL ["/bin/bash", "-c"] 

RUN python3 -m venv env;source env/bin/activate

RUN pip install -r requirements.txt

CMD [ "python3", "-u", "app.py"]
