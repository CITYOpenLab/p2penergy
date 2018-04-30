# p2penergy

## flow

photon -> particle cloud API -> raspberry pi

## usage

```
export FLASK_APP=app.py
flask run
```

## photon power measurements

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

## next steps

* register pi on yale wireless
* get particle cloud data and chart using ChartJS
* user interface wireframe

## relevant REST API endpoints

### /devices

Request:

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
		"id": "34003d000547363332363639",
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

### event stream

```sh
$ curl "https://api.particle.io/v1/devices/0123456789abcdef01234567/events?access_token=1234"
```