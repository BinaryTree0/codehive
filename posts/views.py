from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import (Company, Institution, Post, PostSkill, Profile,
                     ProfileEducation, ProfileExperience, ProfileSkill, Skill,
                     Submission, Task, TaskUser)
from .permissions import IsCompany, IsListDetailOrIsAuthenticated
from .serializers import (CompanySerializer, InstitutionSerializer,
                          PostSerializer, PostSkillSerializer,
                          ProfileEducationSerializer,
                          ProfileExperienceSerializer, ProfileSerializer,
                          ProfileSkillSerializer, SkillSerializer,
                          SubmissionSerializer, TaskListSerializer,
                          TaskSerializer, TaskUserSerializer)


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsCompany, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ProfileSkillViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        return ProfileSkill.objects.filter(profile=self.kwargs['profile_pk'])


class ProfileEducationViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        return ProfileEducation.objects.filter(profile=self.kwargs['profile_pk'])


class ProfileExperienceViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        return ProfileExperience.objects.filter(profile=self.kwargs['profile_pk'])


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer


class TaskUserViewSet(viewsets.ModelViewSet):
    queryset = TaskUser.objects.all()
    serializer_class = TaskUserSerializer


class PostSkillViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        return PostSkill.objects.filter(profile=self.kwargs['post_pk'])


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsListDetailOrIsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def perform_create(self, serializer):
        company = get_object_or_404(Company, user=self.request.user)
        serializer.save(company=company)


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
