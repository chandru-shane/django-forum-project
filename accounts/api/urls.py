from django.urls import path

from . import views

app_name = "customuser"

urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("login/", views.CreateTokenView.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
]
