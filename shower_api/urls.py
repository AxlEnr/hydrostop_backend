from django.urls import path
from . import views

urlpatterns = [
    path('showers', views.get_all_showers),
    path('showers/create', views.create_showers),
    path('showers/update', views.update_showers),
    path('showers/delete', views.delete_showers),
    path('shower/config/<int:shower_id>/', views.get_shower_config, name='get_shower_config'),
    path('shower/update/<int:shower_id>/', views.update_shower_config, name='update_shower_config'),
]