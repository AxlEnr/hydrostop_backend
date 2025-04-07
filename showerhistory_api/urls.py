from django.urls import path
from . import views

urlpatterns = [
    path('shower-history/start/', views.start_shower_session, name='start_shower_session'),
    path('shower-history/end/<int:history_id>/', views.end_shower_history, name='end_shower_session'),

    path('showerhistory/', views.get_histories),
    path('shower-history/end/<int:history_id>/', views.end_shower_history, name='end_shower_history'),
    # ... tus otras URLs existentes
]