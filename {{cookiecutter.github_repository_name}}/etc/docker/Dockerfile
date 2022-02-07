FROM python:3.10
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /app/
WORKDIR /app/
ENV HOME /app
ADD src/ /app