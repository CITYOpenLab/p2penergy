# Photon

Makes power measurements and transmits the data to a central server.

<!-- TOC -->

- [Photon](#photon)
    - [Code](#code)
    - [Development/testing](#developmenttesting)
    - [Deploying to a product](#deploying-to-a-product)
    - [Typical power measurements](#typical-power-measurements)

<!-- /TOC -->

## Code

The source code can be found in the [../photon](https://github.com/CITYOpenLab/p2penergy/tree/master/photon) directory.

The following resources were used to write the power monitor:

1. https://www.hackster.io/ShawnHymel/hack-your-home-part-3-power-monitor-16a313
2. https://www.hackster.io/mjrobot/python-webserver-with-flask-and-raspberry-pi-41b5fc

## Development/testing

Visit [https://build.particle.io/build](https://build.particle.io/build) to write code in the online editor and flash to a device over the Internet.

## Deploying to a product

View [https://docs.particle.io/guide/tools-and-features/console/#product-tools](https://docs.particle.io/guide/tools-and-features/console/#product-tools) for information on how to deploy a firmware to a fleet of devices.

## Typical power measurements

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
