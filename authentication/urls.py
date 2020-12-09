from django.urls import path

from authentication.views import (
    AuthLoginView, AuthLogoutView, 
    AuthRegisterView,
    AuthPasswordResetView,
    PasswordChangeView,
    ProfileView,
    )

urlpatterns = [
    path(
        "account/login/",
        AuthLoginView.as_view(),
        name="login",
    ),
    path(
        "account/logout/",
        AuthLogoutView.as_view(),
        name="logout",
    ),
    path(
        "account/register/",
        AuthRegisterView.as_view(),
        name="register",
    ),
    path(
        "account/change_password/",
        PasswordChangeView.as_view(),
        name="change_password",
    ),
    path(
        "account/profile/",
        ProfileView.as_view(),
        name="profile",
    ),
    path(
        "account/password_reset/",
        AuthPasswordResetView.as_view(),
        name="password_reset",
    ),
]
