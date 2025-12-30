import django

django.setup()

import settings
import importlib

SessionStore = importlib.import_module(settings.SESSION_ENGINE).SessionStore()
from django.contrib.sessions.models import Session

x = Session.objects.all()
print(x)
