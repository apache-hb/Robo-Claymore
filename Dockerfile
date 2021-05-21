FROM python:3.9

WORKDIR /app

# we store requirements seperatley so docker can cache it
COPY data/requirements.txt .

RUN pip install -r requirements.txt

# copy in and run the bot
COPY bot .
CMD [ "python", "main.py" ]
