FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
# CMD ["gunicorn", "-b", "0.0.0.0:5003", "main:app"]
