# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
EXPOSE 3000

RUN pip install --upgrade pip

WORKDIR /app

ADD templates templates
COPY templates .
COPY rallyleads.json .
COPY sosrallycalc.py .

SHELL ["/bin/bash", "-c"] 

RUN python3 -m venv env;source env/bin/activate

RUN pip install flask

CMD [ "python3", "-u", "sosrallycalc.py"]
