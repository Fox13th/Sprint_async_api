FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r /app/requirements.txt --no-cache-dir

COPY . /app

WORKDIR /app
