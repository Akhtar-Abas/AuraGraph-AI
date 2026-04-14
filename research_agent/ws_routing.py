from django.urls import re_path
from platform_api.consumers import ResearchConsumer

websocket_urlpatterns = [
    # Is path ko dhyan se dekhein
    re_path(r'ws/research/$', ResearchConsumer.as_asgi()), 
]