FROM python:3.12-slim

ENV DJANGO_PUBLIC_ROOT /srv/
ENV APP_HOME /usr/local/app

RUN apt-get update && \
    apt-get install -y python3-gdal gettext wait-for-it && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir $APP_HOME
RUN mkdir -p $DJANGO_PUBLIC_ROOT/media $DJANGO_PUBLIC_ROOT/static
WORKDIR $APP_HOME
COPY pyproject.toml $APP_HOME/
COPY poetry.lock $APP_HOME/
RUN pip install -U pip wheel setuptools poetry
RUN poetry install --no-root --with server
COPY ausgsteckt $APP_HOME
RUN poetry run python manage.py collectstatic --noinput
RUN poetry run python manage.py compilemessages
COPY docker/docker-entrypoint.sh /

EXPOSE 8000
VOLUME $DJANGO_PUBLIC_ROOT
ENTRYPOINT ["/docker-entrypoint.sh"]
