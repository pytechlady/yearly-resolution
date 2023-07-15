from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import *

app_name = "user"
router = DefaultRouter()

router.register(r"users", UserViewset, basename="users")
router.register(r"auth", AuthenticationViewset, basename="auth")
router.register(r"forgot", ForgotPasswordViewset, basename="forgot-password")

urlpatterns = [
    path("", include(router.urls)),
]