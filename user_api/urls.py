from django.urls import path
from . import views
from .views import LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users/', views.get_all_users, name='get_users'),
    path('users2/', views.get_all_users_a, name='get_users2'),
    path('user/', views.get_user, name='get_user'),
    path('users/signup/', views.signup, name='signup'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/deactivate/<int:user_id>/', views.delete_user, name='deactivate_user'),
    path('users/activate/<int:user_id>/', views.activate_user, name='activate_user'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/change_password/', views.change_password, name='change_password'),
    path('users/request_password_reset/', views.request_password_reset, name='request_password_reset'),
]