from django.urls import path, include
from rest_framework.routers import DefaultRouter
from goals.views import *


app_name = 'goals'
router = DefaultRouter()
router.register(r'goals', GoalViewset, basename='goals')
router.register(r'user_goals', UserGoalViewset, basename='user-goals')




urlpatterns = [
    path('', include(router.urls)),
]
