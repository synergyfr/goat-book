from django.urls import path
from lists import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path('lists/the-only-list-in-the-world/', views.view_list, name='view_list'),
]
