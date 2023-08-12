from django.contrib import admin
from .models import Reward, UserReward

# Register your models here.
class RewardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'point', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    
admin.site.register(Reward, RewardAdmin)

class UserRewardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'reward', 'point', 'is_claimed')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'reward', 'is_claimed')
    
admin.site.register(UserReward, UserRewardAdmin)
