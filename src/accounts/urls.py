from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views

urlpatterns = [
    path('send_login_email', views.send_login_email, name="send_email"),
    path('login', views.login, name="login"),
    path('logout', auth_views.LogoutView.as_view(next_page='/'), name="logout"),
]
