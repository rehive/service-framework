FROM python:3.6

ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy application code to the container
RUN mkdir /app/
WORKDIR /app/
ENV HOME /app
ENV PATH /venv/bin:$PATH
ADD src/ /app
