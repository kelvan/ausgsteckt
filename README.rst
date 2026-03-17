==========
ausgsteckt
==========

Requirements
============

* Python 3.12+
* PostgreSQL with PostGIS
* Node.js / npm

Quickstart
==========

.. code-block:: bash

    npm install
    uv sync --group dev
    createdb ausgsteckt
    cd ausgsteckt
    python manage.py migrate
    python manage.py runserver

Docker
======

.. code-block:: bash

    cp config.yaml.example config.yaml  # adjust as needed
    docker compose up

Code Quality
============

.. code-block:: bash

    uvx ruff check .
    uvx ruff format .
    uvx ty check
