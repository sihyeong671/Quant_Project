FROM python:3.9.0

COPY ./ /home/ubuntu/quant_server

WORKDIR /home/ubuntu/quant_server/

RUN apt-get upgrade && pip3 install --upgrade pip

RUN pip install -r requirements.txt

RUN pip install gunicorn

EXPOSE 8000
EXPOSE 8001
EXPOSE 8002
EXPOSE 8003

EXPOSE 8080
EXPOSE 8081
