from typing import Set
from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField
from rewards.models import Reward

# Create your models here.

class Goal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name   
    
    
class UserGoal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='user_id')
    goal = models.CharField(max_length=255)
    category = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='user_category')
    start_date = models.DateField()
    end_date = models.DateField()
    blockers = ArrayField(models.CharField(max_length=255), default=list)
    friend = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='user_friend', blank=True, null=True)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='user_price', blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.goal
    

class Friend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='the_referral')
    friend = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='referred_user', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.friend.first_name +'' + self.friend.last_name
