FROM python:3.14-slim

ENV APP_HOME /usr/local/app

RUN apt-get update && \
    apt-get install -y python3-gdal gettext npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir $APP_HOME
RUN mkdir -p $DJANGO_PUBLIC_ROOT/media $DJANGO_PUBLIC_ROOT/static
WORKDIR $APP_HOME
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml $APP_HOME/
COPY uv.lock $APP_HOME/
RUN uv sync --no-dev --group server
COPY package.json package-lock.json /usr/local/
RUN npm install --prefix /usr/local
COPY ausgsteckt $APP_HOME
# Must run after the templates are copied, tailwind scans them for used classes.
RUN /usr/local/node_modules/.bin/tailwindcss \
    -i $APP_HOME/assets/tailwind.css \
    -o $APP_HOME/ausgsteckt/static/css/tailwind.css \
    --minify
RUN uv run python manage.py compilemessages
COPY docker/docker-entrypoint.sh /

EXPOSE 8000
VOLUME /srv
ENTRYPOINT ["/docker-entrypoint.sh"]
