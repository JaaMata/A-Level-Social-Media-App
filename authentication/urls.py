from django.urls import path

from authentication.views import SignupView

urlpatterns = [
    path('signup', SignupView.as_view()),

]
