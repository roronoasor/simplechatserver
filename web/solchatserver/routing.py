from django.urls import path, re_path

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from chatserver.consumers import ChatConsumer

from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({

    # Channels will do this for you automatically. It's included here as an example.
    "http": get_asgi_application(),

    # Route all WebSocket requests to our custom chat handler.
    # We actually don't need the URLRouter here, but we've put it in for
    # illustration. Also note the inclusion of the AuthMiddlewareStack to
    # add users and sessions - see http://channels.readthedocs.io/en/latest/topics/authentication.html
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
        ]),
    ),

})