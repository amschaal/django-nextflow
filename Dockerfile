# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY Makefile /code/
RUN make conda
RUN make install
#COPY requirements.txt /code/
#RUN pip install -r requirements.txt
COPY . /code/
