# research_agent/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'research_agent.settings')

# Initialize Django ASGI application early
django_asgi_app = get_asgi_application()

# Import your routing now
import research_agent.ws_routing 

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            research_agent.ws_routing.websocket_urlpatterns
        )
    ),
})