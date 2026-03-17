FROM python:3.14-slim

ENV DJANGO_PUBLIC_ROOT /srv/
ENV APP_HOME /usr/local/app

RUN apt-get update && \
    apt-get install -y python3-gdal gettext wait-for-it && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir $APP_HOME
RUN mkdir -p $DJANGO_PUBLIC_ROOT/media $DJANGO_PUBLIC_ROOT/static
WORKDIR $APP_HOME
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml $APP_HOME/
COPY uv.lock $APP_HOME/
RUN uv sync --no-dev --group server
COPY ausgsteckt $APP_HOME
RUN uv run python manage.py collectstatic --noinput
RUN uv run python manage.py compilemessages
COPY docker/docker-entrypoint.sh /

EXPOSE 8000
VOLUME $DJANGO_PUBLIC_ROOT
ENTRYPOINT ["/docker-entrypoint.sh"]
