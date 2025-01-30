from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserReview, ReviewReception, Badge

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

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
    user_reaction = serializers.CharField(allow_null=True, read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = UserReview
        fields = ['id', 'rating', 'review', 'created_at', 'user', 'book', 'total_likes', 'total_dislikes', 'user_reaction']
        read_only_fields = ['user', 'total_likes', 'total_dislikes', 'user_reaction']

    def get_user(self, obj):
        return obj.user.username

class ReviewReceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReception
        fields = ['review', 'reaction', 'user']
        read_only_fields = ['user']

    def validate(self, data):
        reaction = data.get('reaction')
        if reaction not in ['like', 'dislike']:
            raise serializers.ValidationError("Reaction must be 'like' or 'dislike'")
        return data

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'