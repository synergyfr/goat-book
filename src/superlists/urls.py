from django.urls import include, path
from lists import views as list_views

urlpatterns = [
    path("", list_views.HomePageView.as_view(), name="home_page"),
    path('lists/', include('lists.urls')),
    path('accounts/', include('accounts.urls'))
]
