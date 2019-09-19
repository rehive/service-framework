FROM python:3.6

ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

RUN mkdir /app \
    && addgroup -S app --gid 400 \
    && adduser -S -g app -h /app -u 400 app \
    && chown -R app:app /app

USER app
WORKDIR /app

COPY --chown=app:app src/ /app
