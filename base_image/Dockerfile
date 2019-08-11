FROM python:3.7-slim-stretch

RUN \
  apt-get update \
  && apt-get autoremove -y \
  && apt-get install -y gcc wget git

WORKDIR /home
COPY requirements.txt .
RUN pip install -r requirements.txt