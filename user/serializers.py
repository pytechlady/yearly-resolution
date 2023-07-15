from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode
from user.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from goals.models import Goal
from rewards.models import Reward


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "id",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        email = attrs.get('email', '')
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')
        password = attrs.get('password', '')

        if not email or not first_name or not last_name or not password:
            raise serializers.ValidationError('Please enter all fields')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserProfile(serializers.ModelSerializer):
    goals = serializers.SlugRelatedField(
        queryset=Goal.objects.all(), many=True, slug_field="name"
    )
    rewards = serializers.SlugRelatedField(
        queryset=Reward.objects.all(), many=True, slug_field="name"
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "goals",
            "success_criteria",
            "rewards",
            "commitment",
            "blocker",
            "referral_link",
            "referred_by",
            "is_verified",
            "created_at",
            "updated_at",
        )


class UserUpdate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")
        read_only_fields = ("id",)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")


class OnboardingSerializer(serializers.ModelSerializer):
    goals = serializers.SlugRelatedField(
        queryset=Goal.objects.all(), many=True, slug_field="name"
    )
    rewards = serializers.SlugRelatedField(
        queryset=Reward.objects.all(), many=True, slug_field="name"
    )

    class Meta:
        model = User
        fields = (
            "goals",
            "success_criteria",
            "rewards",
            "commitment",
            "blocker",
        )


class SendEmailVerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=True, required=False)
    
    class Meta:
        model = User
        fields = ("email",)


class VerifyEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=True, required=False)
    
    class Meta:
        model = User
        fields = ("email", "otp")


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=True, required=False)
    
    class Meta:
        model = User
        fields = ("email",)
        

class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("password", "confirm_password")

