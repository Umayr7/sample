from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-view'),
    # path('compress/', views.compress, name='compress-view')
]