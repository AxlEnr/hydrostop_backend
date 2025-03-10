from django.urls import path
from . import views

urlpatterns = [
    path('showers', views.get_all_showers),
    path('showers/create', views.create_showers),
    path('showers/update', views.update_showers),
    path('showers/delete', views.delete_showers)
]