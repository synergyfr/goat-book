from django.urls import include, path
from lists import views as list_views

urlpatterns = [
    path("", list_views.home_page, name="home_page"),
    path('lists/', include('lists.urls')),
]
