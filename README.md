# P2P Energy

## Usage

Activate virtualenv:

```
source ~/.virtualenv/p2penergy/bin/activate
```

Navigate to source code:

```
cd ~/Developer/p2penergy
```

Run Flask:

```
export FLASK_APP=app.py
flask run
```

## Photon Power measurements

* Base/noise: 5.5 W
* Photon: 0.3 W
* Microwave Power 10: 2000 W
* Microwave Power 6: 1200 W
* Microwave Power 3: 700 W
* Fridge Door Open, Light On, Cooler Off: 35 W
* Fridge Door Open, Cooler On: 160 W (including light )
* Fridge Door Closed, Light Off, Cooler Off: 20 W
* Fridge Cyclic Surge/Startup: 840 W, 6.5 A (after every minute for 20 seconds)
* Raspberry Pi Zero W: 1 W

## Resources used

1. https://www.hackster.io/ShawnHymel/hack-your-home-part-3-power-monitor-16a313
2. https://www.hackster.io/mjrobot/python-webserver-with-flask-and-raspberry-pi-41b5fc

## Getting data from the Photons to the Raspberry Pi

An overview of some techniques is below. 

### Particle Device Cloud API

The Cloud API is a REST API. The Pi server can make repeated `GET` requests to Particle devices and/or their exposed variables. However, polling for new data can be inefficient. 

A small example:

```sh
curl --request GET \
  --url https://api.particle.io/v1/devices \
  --header 'authorization: Bearer 1234453465' \
  --header 'content-type: application/json'
```

Response: 

```js
[
	{
		"id": "34003d00054733639",
		"name": "ENAS130",
		"last_app": null,
		"last_ip_address": "130.132.173.170",
		"last_heard": "2018-04-30T18:07:12.555Z",
		"product_id": 6,
		"connected": false,
		"platform_id": 6,
		"cellular": false,
		"notes": null,
		"status": "normal",
		"current_build_target": "0.7.0",
		"system_firmware_version": "0.7.0",
		"default_build_target": "0.7.0"
	}
]
```

### Webhooks

Webhooks make outgoing HTTP connections to an external server each time an event is received by the Particle Cloud.

Webhooks are easy to setup, but have some important considerations:

* The Cloud has a request cap of 12 calls per minute. This means that the sampling rate cannot be less than 5 seconds.
* The server (in this case, the Raspberry Pi) needs to be reachable over the internet. This requires use of dynamic DNS or a fixed IP address. 
	* Typically, the necessary ports are opened on the router, and if the ISP has assigned a dynamic IP, then a DDNS client is installed on the Pi. The resulting domain name is used as the Webhook callback on Particle Cloud.

### Server-Sent Events (SSEs)

SSEs have your server make an outgoing encrypted TLS/SSL connection to the Particle Cloud and keeps the connection open. The Particle Cloud can then push events down this connection in near real time.

One can observe this event stream using a Terminal:

```sh
$ curl "https://api.particle.io/v1/devices/0123456789abcdef01234567/events?access_token=1234"
```

The connection is uni-directional, which distinguishes it from alternatives like WebSockets. Furthermore, WebSockets is a later protocol, while SSEs take place over HTTP.

Benefits over Webhooks:

* Faster response time.
* Lower request overhead on the Pi server.
* Can receive events at full 1 event per second publish rate per device, instead of the 12 webhook calls per minute maximum.
* The server can be behind a firewall, including NAT.
* The server does not require a DNS name or a fixed IP address.
* The connection is encrypted without requiring a TLS/SSL server certificate for the server.

### Technique used: SSEs

Web-app developers often opt for a Node-Express setup with the official ParticleJS SDK (a wrapper for their REST API), which makes it easy to subscribe to an event stream.

However, the current Flask (a Python web-framework) setup tends to be more readable and emphasizes object-oriented approaches (OOP). The RPi GPIO package is also more mature. Ultimately it comes down to preference and the team's skillset.

We can use the `sseclient-py` package, that uses the popular `Requests` library underneath the hood.

Documentation:

* https://github.com/mpetazzoni/sseclient
* https://stackoverflow.com/questions/29550426/how-to-parse-output-from-sse-client-in-python
* https://docs.particle.io/reference/api/#get-a-stream-of-events


Other considerations:
* Subscribing to SSEs can be done in a separate thread, or with an async job-queue like [Celery](http://www.celeryproject.org/) and a broker like Redis. 
* Database performance in an async context needs evaluation.

## How to contribute

1. Fork the [yalethinkspace/thinkspace-web](https://github.com/CITYOpenLab/p2penergy) repository. Please see GitHub
   [help on forking](https://help.github.com/articles/fork-a-repo) or use this [direct link](https://github.com/yalethinkspace/CITYOpenLab/p2penergy) to fork.
2. Clone your fork to your local machine.
3. Create a new [local branch](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/).
4. Run tests and make sure your contribution works correctly.
5. Create a [pull request](https://help.github.com/articles/creating-a-pull-request) with details of your new feature, bugfix or other contribution.