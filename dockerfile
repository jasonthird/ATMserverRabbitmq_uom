FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apk add mariadb-connector-c-dev gcc musl-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./main.py /app/main.py
COPY ./sqlConfig.json /app/sqlConfig.json
COPY ./SqlConnection.py /app/SqlConnection.py

CMD ["python", "main.py"]