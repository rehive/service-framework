FROM python:3.6

ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy application code to the container
RUN mkdir /app/
WORKDIR /app/
ENV HOME /app
ENV PATH /venv/bin:$PATH
ADD src/ /app

# Migrates the database, uploads staticfiles, and runs the production server
CMD ./manage.py migrate && \
    ./manage.py collectstatic --noinput && \
    gunicorn --bind 0.0.0.0:$PORT --access-logfile - config.wsgi:application
