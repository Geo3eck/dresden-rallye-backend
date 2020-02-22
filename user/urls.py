from django.urls import path
from . import views


urlpatterns = [
    path('api/user/signup/', views.SignUpAPI.as_view(), name='user-signup'),
    path('api/user/signin/', views.SignInAPI.as_view(), name='user-signin'),
]
