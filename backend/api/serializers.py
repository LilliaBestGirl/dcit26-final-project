from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserReview, ReviewReception, Badge, ObtainedBadge

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ReviewSerializer(serializers.ModelSerializer):
    total_likes = serializers.IntegerField(read_only=True)
    total_dislikes = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserReview
        fields = ['id', 'rating', 'review', 'created_at', 'user', 'book', 'total_likes', 'total_dislikes']
        read_only_fields = ['user']

class ReviewReceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReception
        fields = ['review', 'reaction']

    def validate(self, data):
        reaction = data.get('reaction')
        if reaction not in ['like', 'dislike']:
            raise serializers.ValidationError("Reaction must be 'like' or 'dislike'")
        return data

class BadgeSerializer():
    class Meta:
        model = Badge
        fields = ['id', 'badge_name', 'description', 'condition_type', 'threshold', 'tier', 'user']

class ObtainedBageSerializer():
    class Meta:
        model = ObtainedBadge
        fields = ['id', 'date_obtained', 'badge_obtained', 'user']