from django.urls import path
from .views import SignUpView, UserLoginView


app_name = 'auth'
urlpatterns = [
    path('auth/sign_up/', SignUpView.as_view(), name='signup'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
]