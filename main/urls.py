from django.urls import path

from main.views import Home

urlpatterns = [
    path('home', Home.as_view(), name='home'),


]
