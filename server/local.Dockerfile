FROM python:3.9.0

WORKDIR /home/

COPY ./ /home/ubuntu/quant_server

WORKDIR /home/ubuntu/quant_server/

RUN apt-get upgrade && pip3 install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["bash", "-c", \
     "python manage.py makemigrations --settings=config.settings.local && \
      python manage.py migrate --settings=config.settings.local && \
      python manage.py runserver 0.0.0.0:8000 --settings=config.settings.local"]
