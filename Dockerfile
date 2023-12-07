from python:3.10-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache git postgresql-dev gcc libc-dev
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py","runserver", "0.0.0.0:8000"]
