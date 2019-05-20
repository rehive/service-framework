FROM python:3.5-alpine3.8
ADD requirements.txt /requirements.txt

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
            gcc \
            make \
            libc-dev \
            musl-dev \
            linux-headers \
            pcre-dev \
            postgresql-dev \
            zlib-dev \
            jpeg-dev \
            libffi-dev \
            gfortran \
            git \
            curl-dev \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h \
    && pyvenv /venv \
    && /venv/bin/pip install -U pip \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/venv/bin/pip install --no-use-pep517 --no-cache-dir -r /requirements.txt" \
    && runDeps="$( \
            scanelf --needed --nobanner --recursive /venv \
                    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                    | sort -u \
                    | xargs -r apk info --installed \
                    | sort -u \
    )" \
    && apk add --virtual .python-rundeps $runDeps \
    && apk del .build-deps

# Copy application code to the container
RUN mkdir /app/ && addgroup -S app && adduser -S -g app app && chown -R app:app /app
WORKDIR /app/
ENV HOME /app
ENV PATH /venv/bin:$PATH
USER app
ADD src/ /app
