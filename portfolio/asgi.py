# asgi.py

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path

from courses.consumers import NotificationConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(    
            [
                re_path(r"ws/notifications/(?P<int:user_id>\w+)/$", NotificationConsumer.as_asgi())],  # Note the path change to include 'ws'
)  # Use the websocket URL patterns here
    ),
})
