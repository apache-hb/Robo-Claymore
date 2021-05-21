FROM python:3.9

WORKDIR /app

COPY bot .

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]
