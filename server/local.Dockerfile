FROM python:3.9.0

WORKDIR /home/

COPY ./ /home/ubuntu/quant_server

WORKDIR /home/ubuntu/quant_server/

RUN apt-get upgrade && pip3 install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000

EXPOSE 8080
