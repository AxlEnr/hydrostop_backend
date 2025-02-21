from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.get_all_users),
    path('users/signup', views.signup),
    path('users/update/<int:user_id>', views.update_user),
    path('users/delete/<int:user_id>', views.update_user)
]