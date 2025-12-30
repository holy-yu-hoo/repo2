# urls.py
from django.urls import path, register_converter, re_path
from django.views.generic import TemplateView

from . import views

app_name = 'app'

urlpatterns = [
	path('', views.IndexView.as_view(), name = 'index'),
]
