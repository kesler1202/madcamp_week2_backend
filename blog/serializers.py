from rest_framework import serializers
from .models import User, Post, Comment


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'nickname', 'class_group']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create the user through the User model manager
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            nickname=validated_data['nickname'],
            class_group=validated_data['class_group']
            # Add other fields if necessary
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'nickname', 'class_group', 'profile_picture', 'github_url', 'post_count', 'comment_count']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'writer', 'title', 'content', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'writer', 'content', 'created_at']