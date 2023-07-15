from rest_framework import serializers
from goals.models import Goal, UserGoal, Friend
from rewards.models import Reward


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ("id", "name", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class UserGoalSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Goal.objects.all(), slug_field="name"
    )
    reward = serializers.SlugRelatedField(queryset=Reward.objects.all(), slug_field="name")
    friend = serializers.SerializerMethodField()

    class Meta:
        model = UserGoal
        fields = (
            "id",
            "user",
            "goal",
            "category",
            "start_date",
            "end_date",
            "blockers",
            "friend",
            "reward",
            "is_completed",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "friend", "created_at", "updated_at")
        
    def get_friend(self, instance):
        try:
            return instance.friend.first_name + " " + instance.friend.last_name
        except:
            return None
        

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ("id", "friend_name", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
        