from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Post, Task
from .serializers import PostSerializer, PostListSerializer, TaskSerializer, TaskListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer
