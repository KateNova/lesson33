from django.urls import path

from .views import (
    SignUpView,
    SingInView,
    ProfileView,
    PasswordUpdateView
)


urlpatterns = [
    path(
        'signup',
        SignUpView.as_view(),
        name='signup'
    ),
    path(
        'login',
        SingInView.as_view(),
        name='signin'
    ),
    path(
        'profile',
        ProfileView.as_view(),
        name='profile'
    ),
    path(
        'update_password',
        PasswordUpdateView.as_view(),
        name='update_password'
    ),
]
