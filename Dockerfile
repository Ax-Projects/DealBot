FROM python:3.12.0b1-slim
WORKDIR /dealbot

RUN mkdir logs
RUN mkdir data_lists

COPY ./requirements.txt .
COPY ./keys.py .

RUN pip install -r requirements.txt

VOLUME ["/dealbot/data_lists", "/dealbot/logs"]
COPY ./main.py . 
CMD python3 main.py