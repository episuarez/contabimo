FROM python:3.7.9-slim-stretch

LABEL maintainer="Owari Studios"

RUN apt-get update --fix-missing -y && apt upgrade -y
RUN apt-get install wkhtmltopdf -y

EXPOSE 5000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

RUN useradd contabimo && chown -R contabimo:contabimo /app
USER contabimo

CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "3", "--preload", "main:app"]
