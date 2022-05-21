from django.urls import path
from .views import SignUpView, UserLoginView


app_name = 'auth'
urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
]