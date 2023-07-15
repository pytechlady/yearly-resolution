from django.contrib import admin
from .models import User

# Register your models here.
class userAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'created_at', 'updated_at')
    list_display_links = ('id', )
admin.site.register(User, userAdmin)