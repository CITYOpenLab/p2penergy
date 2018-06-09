# Raspberry Pi

Acts as the central server. Receives information from a fleet of Photons. Exposes a web/user interface for access to important metrics.

<!-- TOC -->

- [Raspberry Pi](#raspberry-pi)
    - [Web app](#web-app)
        - [Local setup](#local-setup)
        - [Deploy](#deploy)

<!-- /TOC -->

## Web app

Flask is a microframework that makes it easy to build web apps in Python. It has lots of [documentation](http://flask.pocoo.org/docs/1.0/), and is easy to deploy. 

### Local setup

1. Clone this repository from [http://github.com/CITYOpenLab/p2penergy](http://github.com/CITYOpenLab/p2penergy)
2. Set up a [virtual environment](https://wsvincent.com/install-python3-mac/) (optional but recommended)
3. Install dependencies

```bash
cd p2penergy/pi
pip3 install -r requirements.txt
```

4. Run the Flask built-in server for testing 

```bash
export FLASK_ENV=development
export FLASK_APP=app.y
flask run
```

### Deploy

Typically, in a production setting, a Flask app is served with gunicorn + nginx: [https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux)