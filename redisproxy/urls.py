from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('get/<str:key>', views.get_val, name='get'),
    path('set/<str:key>', views.set_key, name='set'),
]