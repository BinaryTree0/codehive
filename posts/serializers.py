from rest_framework import serializers

from .models import Post, Task


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {'image': {'max_length': 200, 'allow_empty_file': False, 'use_url': True}}


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["image", "title", "created", "summary", "author"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["post", "title", "difficulty", "time_limit"]
