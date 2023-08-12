from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rewards.serializers import RewardSerializer, UserRewardSerializer
from rewards.models import Reward, UserReward


# Create your views here.
class RewardsViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()
    
    @action(methods=['post'], detail=False)
    def create_reward(self, request):
        reward_serializer = self.serializer_class(data=request.data)
        if reward_serializer.is_valid():
            reward_serializer.save()
            return Response(reward_serializer.data, status=status.HTTP_201_CREATED)
        return Response(reward_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['get'], detail=False)
    def get_rewards(self, request):
        rewards = Reward.objects.all()
        if not rewards:
            return Response({"message": "No rewards found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(rewards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=False)
    def get_reward(self, request):
        try:
            reward = Reward.objects.filter(id=request.GET.get('id')).first()
        except Reward.DoesNotExist:
            return Response({"message": "Reward not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(reward)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['PATCH'], detail=False)
    def update_reward(self, request):
        try:
            reward = Reward.objects.filter(id=request.GET.get('id')).first()
            if not reward:
                return Response({"message": "Reward not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.serializer_class(reward, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Reward.DoesNotExist:
            return Response({"message": "Reward not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(methods=['DELETE'], detail=False)
    def delete_reward(self, request):
        try:
            reward = Reward.objects.get(id=request.GET.get('id'))
        except Reward.DoesNotExist:
            return Response({"message": "Reward not found"}, status=status.HTTP_404_NOT_FOUND)
        reward.delete()
        return Response({"message": "Reward deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class UserRewardViewset(viewsets.ModelViewSet):
    serializer_class = UserRewardSerializer
    queryset = UserReward.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_a_reward(self, *args, **kwargs):
        try:
            reward = Reward.objects.get(reward=kwargs['reward'])
            return reward
        except Reward.DoesNotExist:
            return None
    
    @action(methods=['post'], detail=False)
    def create_user_reward(self, request):
        user = request.user
        userReward = self.serializer_class(data=request.data)
        if userReward.is_valid():
            reward = request.data.get('reward')
            reward = self.get_a_reward(reward=reward)
            point = reward.get('point')
            userReward.save(user=user, reward=reward, point=point)
            return Response(userReward.data, status=status.HTTP_201_CREATED)
        return Response(userReward.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['get'], detail=False)
    def get_all_user_rewards(self, request):
        try:
            users_rewards = UserReward.objects.all()
            if not users_rewards:
                return Response({"message": "No users rewards found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.serializer_class(users_rewards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserReward.DoesNotExist:
            return Response({"message": "No users rewards found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(methods=['get'], detail=False)
    def get_user_reward(self, request):
        try:
            user = request.user
            user_reward = UserReward.objects.filter(user=user)
            if not user_reward:
                return Response({"message": "No rewards for this user"}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.serializer_class(user_reward, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserReward.DoesNotExist:
            return Response({"message": "User reward not found"}, status=status.HTTP_404_NOT_FOUND)