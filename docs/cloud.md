# Particle Cloud API

The API is a REST API, and requests are delivered over HTTP. View the full documentation at [https://docs.particle.io/reference/api/](https://docs.particle.io/reference/api/).

<!-- TOC -->

- [Particle Cloud API](#particle-cloud-api)
    - [Access token](#access-token)
        - [Request](#request)
        - [Response](#response)
    - [Receiving events](#receiving-events)
        - [Server-Sent Events](#server-sent-events)
            - [Get event stream for a product](#get-event-stream-for-a-product)
                - [Definition](#definition)
                - [Request](#request-1)
                - [Response](#response-1)
            - [Get event stream for a specific device in a product](#get-event-stream-for-a-specific-device-in-a-product)
                - [Definition](#definition-1)
                - [Request](#request-2)
                - [Response](#response-2)
            - [Packages to read event streams](#packages-to-read-event-streams)
        - [Webhooks](#webhooks)
            - [Creating a webhook](#creating-a-webhook)
        - [Polling](#polling)

<!-- /TOC -->


## Access token

You may find your current access token on the settings page of [https://build.particle.io/](https://build.particle.io/build/new).

You may list all your access tokens using the API:

### Request

```bash
curl https://api.particle.io/v1/access_tokens -u "joe@example.com:SuperSecret"
```

### Response

```json
GET /v1/access_tokens
HTTP/1.1 200 OK
[
  {
      "token": "b5b901e8760164e134199bc2c3dd1d228acf2d98",
      "expires_at": "2014-04-27T02:20:36.177Z",
      "client": "particle"
  },
  {
      "token": "ba54b6bb71a43b7612bdc7c972914604a078892b",
      "expires_at": "2014-04-27T06:31:08.991Z",
      "client": "particle"
  }
]
```

## Receiving events

Below are multiple strategies to receive events from the API.

You will need to first get your access token, and any pre-requisite IDs, such as a device ID or product ID.

### Server-Sent Events

SSEs allow the developer to make an outgoing encrypted TLS/SSL connection to the Particle Cloud and keep the connection open. The Particle Cloud can then push events down this connection in near real time.

The connection is uni-directional, and has the following benefits:

* Faster response time than webhooks
* Can receive events at full 1 event per second publish rate per device, instead of the 12 webhook calls per minute maximum
* The server can be behind a firewall, including NAT
* The server does not require a DNS name or a fixed IP address
* The connection is encrypted without requiring a TLS/SSL server certificate for the server

#### Get event stream for a product

##### Definition

```
GET /v1/products/:productIdOrSlug/events/[:eventName]
```

##### Request

```bash
curl "https://api.particle.io/v1/products/my-product/events?access_token=1234"
```

##### Response

```bash
GET /v1/products/my-product/events
HTTP/1.1 200 OK
:ok

event: temperature
data: {"data":"25.34","ttl":"60","published_at":"2015-07-18T00:12:18.174Z","coreid":"0123456789abcdef01234567"}
```

#### Get event stream for a specific device in a product

##### Definition

```
GET /v1/products/:productIdOrSlug/devices/:id/events/[:eventName]
```

##### Request

```bash
curl "https://api.particle.io/v1/products/:productIdOrSlug/devices/123abc/events?access_token=1234
```

##### Response

```bash
GET /v1/products/:productIdOrSlug/devices/123abc/events
HTTP/1.1 200 OK
:ok

event: temperature
data: {"data":"25.34","ttl":"60","published_at":"2015-07-18T00:12:18.174Z","coreid":"0123456789abcdef01234567"}
```

#### Packages to read event streams

* The `sseclient-py` package - available at [https://github.com/mpetazzoni/sseclient](https://github.com/mpetazzoni/sseclient) - can be used to read SSE streams in Python. Similar packages are available for other languages
* Subscribing to SSEs can be done in a separate thread, or with an async job-queue like [Celery](http://www.celeryproject.org/) and a broker like Redis

### Webhooks

Webhooks make outgoing HTTP connections to an external server each time an event is received by the Particle Cloud.

Webhooks are easy to setup, but have some important considerations:

* The Cloud has a request cap of 12 calls per minute. This means that the sampling rate cannot be less than 5 seconds
* The server needs to be reachable over the internet. This requires use of dynamic DNS or a fixed IP address
* Typically, the necessary ports are opened on the router, and if the ISP has assigned a dynamic IP, then a DDNS client is installed on the server. The resulting domain name is used as the Webhook callback on Particle Cloud

#### Creating a webhook

Navigate to `https://console.particle.io/:productID/integrations` where you will be able to create a webhook integration for the given product.

### Polling

Variable values can also be read using one-off GET requests. However, this is not recommended.

For an example, visit [https://docs.particle.io/reference/api/#get-a-variable-value](https://docs.particle.io/reference/api/#get-a-variable-value).