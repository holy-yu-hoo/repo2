import django

django.setup()

from django.contrib.auth.models import User, AbstractUser, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from app.models import Universe
from django.contrib.auth.decorators import login_required

# content_type = ContentType.objects.get_for_model(Universe)
user_permissions = Permission.objects
# print(user_permissions)
user = authenticate(username = "yura", password = "12345")

# user.user_permissions.add(*user_permissions)
