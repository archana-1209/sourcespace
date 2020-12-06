from django.urls import path

from . import views

app_name = "authentication"

urlpatterns = [
    path(
        "/account/login/",
        views.AuthLoginView.as_view(),
        name="login",
    ),
    path(
        "/account/logout/",
        views.AuthLogoutView.as_view(),
        name="logout",
    ),
    path(
        "/account/register/",
        views.register_view,
        name="register",
    ),
    path(
        "/account/change_password/",
        views.change_password_view,
        name="change_password",
    ),
    path(
        "/account/profile/",
        views.profile_view,
        name="profile",
    ),
    path(
        "/account/password_reset/",
        views.AuthPasswordResetView.as_view(),
        name="password_reset",
    ),
]
