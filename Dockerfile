FROM ubuntu:jammy

RUN mkdir logs
RUN mkdir data_lists
COPY ./requirements.txt .
COPY ./keys.py .

RUN apt update
RUN apt install python3 python3-pip unzip -y

RUN pip install -r requirements.txt

COPY ./main.py . 
CMD python3 main.py