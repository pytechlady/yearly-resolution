from django.contrib import admin
from .models import Goal, Friend, UserGoal

# Register your models here.
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    
admin.site.register(Goal, GoalAdmin)

class FriendAdmin(admin.ModelAdmin):
    list_display = ('id', 'friend', 'created_at', 'updated_at')
    list_display_links = ('id', 'friend')
    
admin.site.register(Friend, FriendAdmin)

class UserGoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'goal', 'category', 'start_date', 'end_date', 'friend', 'reward', 'is_completed')
    list_display_links = ('id', 'user', 'goal')
    
admin.site.register(UserGoal, UserGoalAdmin)