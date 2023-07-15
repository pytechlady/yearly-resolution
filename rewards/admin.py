from django.contrib import admin
from .models import Reward

# Register your models here.
class RewardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'point', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    
admin.site.register(Reward, RewardAdmin)
