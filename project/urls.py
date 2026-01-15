from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from . import settings

handler400 = views.Error400View.as_view()
handler403 = views.Error403View.as_view()
handler404 = views.Error404View.as_view()
handler500 = views.Error500View.as_view()

urlpatterns = [
	path('admin/', admin.site.urls),
	# path('',
	# 	include(('app.urls', 'app')),
	# ),
	path('main/', include(('main.urls', 'main')), ),
	path('', views.index, name = 'index'),
	path("app/", include(("app.urls", "app"))),
	# static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
