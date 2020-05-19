FROM python:3.7

ENV DJANGO_PUBLIC_ROOT /srv/
ENV APP_HOME /usr/local/app

RUN apt-get update
RUN apt-get install -y python3-gdal gettext
RUN apt-get install wait-for-it

RUN mkdir $APP_HOME
RUN mkdir -p $DJANGO_PUBLIC_ROOT/media $DJANGO_PUBLIC_ROOT/static
WORKDIR $APP_HOME
COPY requirements $APP_HOME/requirements
RUN pip install -U pip wheel setuptools
RUN pip install -r requirements/server.txt
COPY ausgsteckt $APP_HOME
RUN python manage.py collectstatic --noinput
RUN python manage.py compilemessages
COPY docker/docker-entrypoint.sh /

EXPOSE 8000
VOLUME $DJANGO_PUBLIC_ROOT
ENTRYPOINT ["/docker-entrypoint.sh"]
