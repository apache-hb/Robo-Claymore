FROM alpine:3.9

RUN apk add --no-cache mongodb python3

RUN python3 -m pip install -r requirements.txt

CMD cd source && python main.py
