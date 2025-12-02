# urls.py
from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name = 'index'),
	path('search/', views.search, name = 'xss_vulnerable'),  # xss search
	path('search_2/', views.search_2, name = 'sql_injection'),  # sql_injection
	path('request_universe/', views.request_universe, name = 'sql_injection_filter'),
	path('csrf-form/', views.csrf_vulnerable_form_view, name = 'csrf_vulnerable_form'),
	path('character/<int:character_id>/', views.character_detail_xss, name = 'character_detail_xss'),
]
