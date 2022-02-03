FROM python:3.9.0
RUN apt-get update 
RUN apt-get -y install curl vim wget python3-pip
COPY requirements.txt /
RUN python3 -m pip install -r requirements.txt
WORKDIR /app
COPY ./ /app/
CMD ["python3.9", "app.py"]

