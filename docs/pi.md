# Raspberry Pi

Acts as the central server. Receives information from a fleet of Photons. Exposes a web/user interface for access to important metrics.

<!-- TOC -->

- [Raspberry Pi](#raspberry-pi)
    - [Web app](#web-app)
        - [Setup](#setup)
            - [Flask](#flask)
            - [Database](#database)
            - [Background jobs](#background-jobs)
        - [Routes](#routes)
        - [MQTT client](#mqtt-client)
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
    flask run
    ```

    FLASK_ENV tells Flask whether or not to run in debug mode (which reloads the server whenever the source code is changed).

    FLASK_APP refers to the Flask app that will be run.

#### Database

Sqlite3 is an embeddable database that does not require a server. 

Carru out first-time database creation as follows:

```bash
flask db init
flask db migrate
flask db upgrade
```

For subsequent model changes, just do:

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

#### Background jobs

Using Celery, in conjunction with a broker like Redis, Flask is able to execute background tasks.

If you would like to make use of functions that run in the background using Celery, you must:

1. Install Redis. On macOS, you can use Homebrew

    ```bash
    brew install redis 
    ```

    For other platforms, see: [https://redis.io/topics/quickstart](https://redis.io/topics/quickstart)

2. Run the Redis broker in a new Terminal

    ```bash
    redis-server
    ```

3. Run a Celery worker a new Terminal

    ```bash
    celery worker -A celery_worker.celery --loglevel=info
    ```

4. Start the Flask app

    ```bash
    cd p2penergy/pi
    export PARTICLE_ACCESS_TOKEN=0123456abcdef
    flask run
    ```

    Here, `PARTICLE_ACCESS_TOKEN` is used to access the Server-Sent Events stream from the [Particle Cloud API](cloud.md).


### Routes

Currently, only a few routes are functional.

1. /

    A home page.

1. /admin

    This route is the homepage for the dashboard. Currently, if you navigate to it, a repeated AJAX call will update the page with the five most recent events stored on the database.

2. /test/event-stream

    If Redis and a Celery worker are running, navigating to this page will start collecting data from the Particle Cloud API Server-Sent Events stream.

### MQTT client

The web app can accept messages over MQTT. To setup for use with a broker, export the following variables before running:

```bash
export MQTT_BROKER_URL= # defaults to broker.hivemq.com, a free online broker for testing
export MQTT_BROKER_PORT= # defaults to 1883
export MQTT_TLS_ENABLED= # defaults to False
export MQTT_KEEPALIVE= # defaults to 5
export MQTT_USERNAME=  # defaults to ''
export MQTT_PASSWORD= # defaults to ''
```

The subscribed topics may be set in `app.py`. Currently, the app subscribes to:

```
p2penergy/photon
```

Future code updates will incorporate Flask-SocketsIO for bi-directional communication.

### Deploy

Typically, in a production setting, a Flask app is served with gunicorn + nginx: [https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux)