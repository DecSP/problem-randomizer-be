"""
ASGI config for My Awesome Project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""
import os
import sys
from pathlib import Path

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# This allows easy placement of apps within the interior
# my_awesome_project directory.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "problem_randomizer_be"))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# This application object is used by any ASGI server configured to use this file.
django_application = get_asgi_application()
# Apply ASGI middleware here.
# from helloworld.asgi import HelloWorldApplication
# application = HelloWorldApplication(application)

from problem_randomizer_be.websocket.urls import websocket_urlpatterns  # noqa

application = ProtocolTypeRouter(
    {
        "http": django_application,
        "websocket": URLRouter(websocket_urlpatterns),
    }
)
