from django.urls import path

from authentication.views import SignupView, VerifyEmailView, LoginView, LogoutView, ResendVerifictaionEmailView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', SignupView.as_view(), name='signup'),
    path('verify-email/<str:token>', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification-email', ResendVerifictaionEmailView.as_view(), name='resend-verify-email'),

]