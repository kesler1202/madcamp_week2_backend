from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Post, Comment

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'nickname', 'class_group', 'profile_picture', 'github_url']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserRegistrationSerializer, self).create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'nickname', 'class_group', 'profile_picture', 'github_url', 'post_count',
                  'comment_count']
        extra_kwargs = {'email': {'read_only': True}}

    def get_post_count(self, obj):
        return Post.objects.filter(writer=obj).count()

    def get_comment_count(self, obj):
        return Comment.objects.filter(writer=obj).count()

class PostSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)

    class Meta:
        model = Post
        # fields = ['id', 'writer', 'title', 'content', 'created_at']
        fields = ['id', 'writer', 'title', 'content', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'writer', 'content', 'created_at']