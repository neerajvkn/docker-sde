FROM ubuntu:18.04
RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y
RUN pip install requests -y

COPY requirements.txt requirements.txt
COPY flaskproj /opt/

RUN pip install -r requirements.txt

WORKDIR /opt/

CMD ["gunicorn3","-b", "0.0.0.0:8000","app:app", "--wrokers=5"]