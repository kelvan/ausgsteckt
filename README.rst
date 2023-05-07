==========
ausgsteckt
==========

Requirements
============

* python >= 3.8
* postgresql with postgis
* see requirements.txt (dev libs like image stuff for easythumbnails, ...)

Quickstart
==========

* npm install
* poetry install  # --with dev,docs,server,test
* createdb ausgsteckt
* cd ausgsteckt
* python manage.py migrate
* python manage.py runserver
