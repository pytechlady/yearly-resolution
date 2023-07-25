from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from goals.models import Goal, UserGoal, Friend
from user.models import User
from goals.serializers import GoalSerializer, UserGoalSerializer, FriendSerializer
from rewards.models import Reward, UserReward

# Create your views here.


class GoalViewset(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()

    @action(methods=["post"], detail=False)
    def create_goal(self, request):
        GoalSerializer = self.serializer_class(data=request.data)
        if GoalSerializer.is_valid():
            GoalSerializer.save()
            return Response(GoalSerializer.data, status=status.HTTP_201_CREATED)
        return Response(GoalSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False)
    def get_goals(self, request):
        goals = Goal.objects.all()
        if not goals:
            return Response(
                {"message": "No goals found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def get_goal(self, request, id):
        try:
            goal = Goal.objects.filter(id=id).first()
        except Goal.DoesNotExist:
            return Response(
                {"message": "Goal not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(goal)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["PATCH"], detail=False)
    def update_goal(self, request):
        try:
            goal = Goal.objects.filter(id=request.GET.get("id")).first()
            if not goal:
                return Response(
                    {"message": "Goal not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(goal, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Goal.DoesNotExist:
            return Response(
                {"message": "Goal not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(methods=["DELETE"], detail=False)
    def delete_goal(self, request):
        try:
            goal = Goal.objects.get(id=request.GET.get("id"))
        except Goal.DoesNotExist:
            return Response(
                {"message": "Goal not found"}, status=status.HTTP_404_NOT_FOUND
            )
        goal.delete()
        return Response({"message": "Goal deleted"}, status=status.HTTP_200_OK)


class FriendViewset(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()

    @action(methods=["post"], detail=False)
    def create_friend(self, request):
        user = user.User.objects.get(referral_link=request.GET.get("referral_link"))
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False)
    def get_friends(self, request):
        friends = Friend.objects.all()
        if not friends:
            return Response(
                {"message": "No friends found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def get_friend(self, request, id):
        try:
            friend = Friend.objects.get(user=id)
        except Friend.DoesNotExist:
            return Response(
                {"message": "Friend not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(friend)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["DELETE"], detail=False)
    def delete_friend(self, request):
        try:
            friend = Friend.objects.get(id=request.GET.get("id"))
        except Friend.DoesNotExist:
            return Response(
                {"message": "Friend not found"}, status=status.HTTP_404_NOT_FOUND
            )
        friend.delete()
        return Response({"message": "Friend deleted"}, status=status.HTTP_200_OK)


class UserGoalViewset(viewsets.ModelViewSet):
    queryset = UserGoal.objects.all()
    serializer_class = UserGoalSerializer

    def get_a_reward(self, *args, **kwargs):
        try:
            reward = Reward.objects.filter(name=kwargs['reward']).first()
            return {
                "name": reward.name,
                "point": reward.point
            }
        except Reward.DoesNotExist:
            return None

    @action(methods=["post"], detail=False)
    def create_user_goal(self, request):
        try:
            user = request.user
            friend = request.data.get("friend", None)
            reward = request.data.get("reward", None)

            UserGoalSerializer = self.serializer_class(data=request.data)
            if UserGoalSerializer.is_valid(raise_exception=True):
                if friend is not None:
                    friend_array = friend.split()
                    friend_user = User.objects.filter(
                        first_name=friend_array[0], last_name=friend_array[1]
                    )
                    if not friend_user.exists():
                        return Response(
                            {"message": "User does not exist"},
                            status=status.HTTP_404_NOT_FOUND,
                        )
                    friend_user = friend_user.first()
                    if Friend.objects.filter(
                        friend__id=friend_user.id, user__id=user.id
                    ).exists():
                        UserGoalSerializer.save(user=user, friend=friend_user)
                        return Response(
                            UserGoalSerializer.data, status=status.HTTP_201_CREATED
                        )
                    else:
                        return Response(
                            {"message": "Friend does not exist"},
                            status=status.HTTP_404_NOT_FOUND,
                        )
                UserGoalSerializer.save(user=user)

                get_reward = self.get_a_reward(reward=reward)
                if get_reward is None:
                    return Response(
                        {"message": "Reward does not exist"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                # Get the Reward instance with the specified name
                reward_instance = get_object_or_404(Reward, name=get_reward['name'])
                
                # Create the UserReward object with the fetched Reward instance
                user_reward = UserReward.objects.create(user=user, reward=reward_instance, point=get_reward['point'])
                user_reward.save()
                return Response(UserGoalSerializer.data, status=status.HTTP_201_CREATED)
            
            return Response(
                UserGoalSerializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False)
    def get_users_goals(self, request):
        user_goals = UserGoal.objects.all()
        if not user_goals:
            return Response(
                {"message": "No user goals found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(user_goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def get_a_user_goals(self, request):
        try:
            user = request.user
            if user.id:
                user_goals = UserGoal.objects.filter(user=user).order_by("-created_at")
                serializer = self.serializer_class(data=user_goals, many=True)
                serializer.is_valid()  # Perform validation
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"message": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except UserGoal.DoesNotExist:
            return Response(
                {"message": "User goals not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(methods=["PATCH"], detail=False)
    def update_a_user_goal(self, request):
        try:
            user = request.user
            goal_id = request.GET.get("id")

            if user.is_anonymous:
                return Response(
                    {"message": "User not authenticated"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            user_goal = UserGoal.objects.filter(user=user, id=goal_id).first()

            if not user_goal:
                return Response(
                    {"message": "Goal not found"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = self.serializer_class(
                user_goal, data=request.data, partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response({serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": "Error updating goal"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(methods=["DELETE"], detail=False)
    def delete_a_user_goal(self, request):
        try:
            user = request.user
            goal_id = request.GET.get("id")

            if user.is_anonymous:
                return Response(
                    {"message": "User not authenticated"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            user_goal = UserGoal.objects.filter(user=user, id=goal_id).first()

            if not user_goal:
                return Response(
                    {"message": "Goal not found"}, status=status.HTTP_404_NOT_FOUND
                )

            user_goal.delete()

            return Response({"message": "Goal deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": "Error deleting goal"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
