from django.urls import path, include
from rest_framework.routers import DefaultRouter
from goals.views import *


app_name = 'goals'
router = DefaultRouter()
router.register(r'goals', GoalViewset, basename='goals')
router.register(r'user_goals', UserGoalViewset, basename='user-goals')
router.register(r'friends', FriendViewset, basename='friends')




urlpatterns = [
    path('', include(router.urls)),
]
