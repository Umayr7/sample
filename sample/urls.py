from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('compress/', app_views.compression, name='compress'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)