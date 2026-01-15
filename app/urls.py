# urls.py
from django.urls import path, register_converter, re_path
from django.contrib.auth import views as auth_views
from . import views
from . import forms

app_name = 'app'

urlpatterns = [
	path('login/',
		auth_views.LoginView.as_view(template_name = 'app/pages/login.html', form_class = forms.LoginForm, next_page = '/app/'),
		name = 'login'),
	path('', views.index, name = 'index'),
	path('req/', views.ReqView.as_view(), name = 'req'),
	path('logout/', views.logout_view, name = 'logout'),
]
