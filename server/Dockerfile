FROM python:3.9.0

WORKDIR /home/

RUN git clone https://github.com/sihyeong671/Quant_Project.git

WORKDIR /home/Quant_Project/server/

RUN apt-get upgrade && pip3 install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["bash", "-c", \
     "python manage.py makemigrations && \
      python manage.py migrate && \
      python manage.py runserver 0.0.0.0:8000"]
