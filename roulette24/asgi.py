"""
ASGI config for roulette24 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import a_game.routing
import a_room.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roulette24.settings')



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                a_game.routing.websocket_urlpatterns + a_room.routing.websocket_urlpatterns
            )
        )
    )
})
