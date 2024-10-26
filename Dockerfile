FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

CMD ["python", "app.py"]
