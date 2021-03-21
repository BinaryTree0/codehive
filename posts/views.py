from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Post, Task, Result, Company
from .serializers import PostSerializer, PostListSerializer, TaskSerializer, TaskListSerializer, ResultSerializer, CompanySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permissions import IsListDetailOrIsAuthenticated


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsListDetailOrIsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    filter_fields = ('title', 'summary')

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
