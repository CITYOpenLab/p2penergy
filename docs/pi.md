# Raspberry Pi

Acts as the central server. Receives information from a fleet of Photons. Exposes a web/user interface for access to important metrics.

<!-- TOC -->

- [Raspberry Pi](#raspberry-pi)
    - [Web app](#web-app)
        - [Setup](#setup)
            - [Flask](#flask)
            - [Background jobs](#background-jobs)
            - [Database](#database)
            - [Routes](#routes)
        - [Deploy](#deploy)

<!-- /TOC -->

## Web app

Flask is a microframework that makes it easy to build web apps in Python. It has lots of [documentation](http://flask.pocoo.org/docs/1.0/), and is easy to deploy. 

### Setup

1. Clone this repository from [http://github.com/CITYOpenLab/p2penergy](http://github.com/CITYOpenLab/p2penergy)
2. Set up a [virtual environment](https://wsvincent.com/install-python3-mac/) (optional but recommended)

#### Flask

1. Install dependencies for Flask

    ```bash
    cd p2penergy/pi
    pip3 install -r requirements.txt
    ```
    
2. Run the built-in server for testing 

    ```bash
    export FLASK_ENV=development
    export FLASK_APP=app
    export PARTICLE_ACCESS_TOKEN=0123456789abcdef
    flask run
    ```

    FLASK_ENV tells Flask whether or not to run in debug mode (which reloads the server whenever the source code is changed).

    FLASK_APP refers to the Flask app that will be run.

    PARTICLE_ACCESS_TOKEN is a token to connect to the [Particle Cloud API](cloud.md).
    
#### Background jobs

Using Celery or RQ, in conjunction with a broker like Redis, Flask is able to execute background tasks. These packages are more scalable than using cron jobs or threads. 

If you would like to make use of functions that run in the background using Celery, you must:

1. Install Redis broker for background jobs. On macOS, you can use Homebrew.

    ```bash
    brew install redis 
    ```

    For other platforms, see: [https://redis.io/topics/quickstart](https://redis.io/topics/quickstart)

2. Run Redis broker in a new Terminal

    ```bash
    redis-server
    ```

3. Run a Celery worker a new Terminal

    ```bash
    export PARTICLE_ACCESS_TOKEN=0123456789abcdef
    celery worker -A celery_worker.celery --loglevel=info
    ```

#### Database

Sqlite3 is an embeddable database that does not require a server. 

For model changes, use the following set of commands:

```bash
flask db migrate
flask db upgrade 
```

PostgreSQL and MySQL servers have their benefits, but increase overhead on the Pi. In any case, the `DATABASE_URL` may be swapped with any SQL database connection, and the SQlAlchemy ORM will support it.

```bash
export DATABASE_URL=postgresql://...
flask db migrate
flask db upgrade
```

#### Routes

Currently, only two routes are functional.

1. /admin

    This route is the homepage for the admin panel. Currently, if you navigate to it, a repeated AJAX call will update the page with the five most recent events stored on the database.

2. /admin/collect

    If Redis and a celery worker are running, navigating to this page will start collecting data from the Server-Sent Events stream mentioned in the [Particle Cloud API](cloud.md) documentation.


### Deploy

Typically, in a production setting, a Flask app is served with gunicorn + nginx: [https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux)