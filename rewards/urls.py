from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rewards.views import *

app_name = "user"
router = DefaultRouter()

router.register(r"rewards", RewardsViewSet, basename="rewards")
router.register(r"user_rewards", UserRewardViewset, basename="user-rewards")

urlpatterns = [
    path("", include(router.urls)),
]