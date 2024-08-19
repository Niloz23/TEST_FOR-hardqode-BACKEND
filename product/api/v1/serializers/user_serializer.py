from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from users.models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""
    balance = serializers.DecimalField(
        source='balance.amount',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    subscriptions = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'balance', 'subscriptions',
        )

class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    user = CustomUserSerializer(read_only=True)
    course = serializers.StringRelatedField()

    class Meta:
        model = Subscription
        fields = (
            'id', 'user', 'course', 'subscribed_at', 'is_active',
        )
