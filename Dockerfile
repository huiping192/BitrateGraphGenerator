FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "app.py"]