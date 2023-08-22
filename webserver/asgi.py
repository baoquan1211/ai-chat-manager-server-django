"""
ASGI config for django_socketio project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from socket_io.urls import urlpatterns
from socket_io.views import app as socket_app
import socketio
import uvicorn
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_socketio.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # "websocket": AuthMiddlewareStack(URLRouter(urlpatterns)),
        "websocket": socket_app,
    }
)
# sio.attach(django_app)
# uvicorn.run(application, reload=True)
# application = ProtocolTypeRouter(
#     {
#         "http": django_asgi_app,
#         # Just HTTP for now. (We can add other protocols later.)
#     }
# )
