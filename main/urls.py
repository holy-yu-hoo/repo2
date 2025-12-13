from django.urls import path, include, reverse
from . import views

app_name = 'main'
urlpatterns = [
	path('', views.index, name = 'index'),
	path('registration/', views.user_registration_view, name = 'registration'),
	path('login/', views.user_login_view, name = 'login'),
	path('user/<slug:login>/home', views.user_home_page_view, name = 'user_home'),
	path('user/<slug:login>/home_edit/', views.user_home_page_edit_view, name = 'user_home_edit'),
	path('logout/', views.user_logout_view, name = 'logout'),
	path('search/', views.search_view, name = 'search'),

]
