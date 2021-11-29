# simplechatserver

This is a simple chat server that can be easily deployed in the latest 
macOS or Linux.


It provides capabilities for a user to register, login, create chat rooms,
send messages to other users in the chatroom, etc.

The server also provides chat persistence.

## Installation

Install the chat server using docker-compose
```
docker-compose build
docker-compose up -d
```
The chat server is to be accessed at [localhost/chat](http://localhost/chat)

To stop the chat server, run
```
docker-compose down
```

## Usage

1. Accessing the server for first time at [http://localhost/chat/](http://localhost/chat/) will prompt the user to login
2. The Login page also provides a hyperlink to register if the user does not have an account in the chat server.
3. Once the user logs in, the user will be provided a form to create a new room
4. The created room url may alse be directly used to login.
5. The chatroom provides an Info button to see actively logged in users.


## How it works

simplechatserver is powered by Django Channels, channels_redis, Daphne, Mongo DB and nginx

All HTTP and Websocket connections are proxied though nginx to a daphne server.

Daphne server runs as the HTTP and Websocket termination server in the django app

The django app uses Django Channels as it natively provides capabilities to handle asynchronous 
connections over HTTP and Websocket.

This chat server uses HTTP for user registration, authentication and navigation, 
Webocket for communication between chat client and chat server, channels_redis
for communication between django channels(consumers) 
and Mongo DB for chat persistence.

The django app uses mongoengine to work with Mongo DB.

Currently, connection pooling is not implemented in the app but it can be used by
providing maxPoolSize argument in mongoengine.connect() method.
mongoengine uses Pymongo to connect to Mongo DB. 

Pymongo supports connecting pooling through maxPoolSize parameter as documeted in
https://api.mongodb.com/python/3.2.1/faq.html#how-does-connection-pooling-work-in-pymongo

## Roadmap

The app can be furter enhanced to provide the following features

### Enhanced Security

HTTPS and wss can be made use of for secure connections between Chat clients and Chat Server over HTTP and Websocket respectively.
[Let's Encrypt](https://letsencrypt.org/getting-started/) can be leveraged to secure the django app as shell access is available.

Further, inter django channels(consumers) communication through channels-redis can be made secure
through the use of symmetric encryption keys as documented in https://github.com/django/channels_redis

Password authentication can be replaced with a token based authentication along with Federated Access.

### Sudden traffic spikes

nginx can be used to load balance traffic between chat servers.
Currently, the chatserver is deployed as a single container. It can be enhanced to provide horizontal scaling
with nginx load balancing the web traffic across the chatserver containers.
Current session based authentication could be a challenge in scaling horizontally.
Token based authentication can solve it better.

If the app is hosted in AWS or GCP, incoming and active HTTP and ws sessions can be monitored 
to increase or decrease the number of containers 

### Federated access

The django app can be integrated with an LDAP Directory or SSO can be enabled through SAML 2.0 with an IDP.

The App may be integrated with AWS or GCP IAM as well.  
[This](https://aws.amazon.com/blogs/security/how-to-implement-federated-api-and-cli-access-using-saml-2-0-and-ad-fs/) example guide may be used to have federated access with AWS.

