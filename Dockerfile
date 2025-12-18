FROM python:3.12-slim

RUN apt-get update && apt-get install -y build-essential libpq-dev

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY backend/ .

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
