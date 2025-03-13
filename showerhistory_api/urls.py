from django.urls import path
from . import views
urlpatterns = [
    path('showerhistory', views.get_all_histories),
    path('showerhistory/create', views.create_history),
    path('showerhistory/update', views.update_history),
    path('showerhistory/delete', views.delete_history)
]