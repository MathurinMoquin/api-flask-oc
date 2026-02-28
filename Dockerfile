FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5003

ARG APP_VERSION=dev
ENV APP_VERSION=$APP_VERSION

CMD ["python3", "main.py"]
# CMD ["gunicorn", "-b", "0.0.0.0:5003", "main:app"]
