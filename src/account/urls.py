from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("", views.LoginUserView.as_view(), name="login"),
    path("logout/", views.LogoutUserView.as_view(), name="logout"),
    path(
        "organizations/",
        views.OrganizationViewList.as_view(),
        name="organizations",
    ),
    path("users/add-user", views.CreateUserView.as_view(), name="add_user"),
    path("users/", views.ListUserView.as_view(), name="list"),
    path("<int:pk>/change/", views.UpdateUserView.as_view(), name="change"),
    path(
        "users/password-user/<int:pk>",
        views.UpdateUserPassword.as_view(),
        name="change_password_user",
    ),
]
