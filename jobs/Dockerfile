FROM python:2.7
MAINTAINER Marcus Lacerda "marcus.lacerda@gmail.com"

# docker build -t ciandt-profile-jobs .
# docker run --rm -v "$PWD":/app ciandt-profile-jobs:latest test.py

RUN mkdir /app

RUN apt-get update
RUN apt-get install -y curl
#RUN apt-get install -y python-pip python-lxml
ADD requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

ENTRYPOINT ["python"]
