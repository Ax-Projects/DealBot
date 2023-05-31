FROM python:3.12.0b1-slim
WORKDIR /dealbot

RUN mkdir logs data_lists

COPY ./requirements.txt .
COPY ./SearchesList.json /dealbot/data_lists
COPY ./keys.py .

RUN pip install --no-cache-dir -r requirements.txt

VOLUME ["/dealbot/data_lists", "/dealbot/logs"]
COPY ./main.py . 
CMD ["python3", "main.py"]