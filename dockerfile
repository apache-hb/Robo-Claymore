FROM python:3.9-buster

RUN pip insrall -r requirements.txt

CMD cd source && python main.py