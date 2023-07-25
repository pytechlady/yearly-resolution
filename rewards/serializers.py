from rest_framework import serializers
from rewards.models import Reward, UserReward


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
        
class UserRewardSerializer(serializers.ModelSerializer):
    reward = serializers.SlugField(source='reward.name')
    
    class Meta:
        model = UserReward
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')