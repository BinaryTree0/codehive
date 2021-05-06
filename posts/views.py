from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import (Company, Institution, Post, PostSkill, Profile,
                     ProfileEducation, ProfileExperience, ProfileSkill, Skill,
                     Submission, Task, TaskUser)
from .permissions import (CreateOnly, IsAdmin, IsAuthenticated, IsCompany,
                          IsCompanyOwner, IsOwner, IsPostOwner, IsProfileOwner,
                          ReadOnly)
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
    permission_classes = [IsAdmin | ReadOnly, ]
    authentication_classes = [TokenAuthentication, ]


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated & IsCompany & IsOwner | IsAdmin | ReadOnly, ]
    authentication_classes = [TokenAuthentication, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdmin | ReadOnly, ]


class ProfileSkillViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated & IsProfileOwner | IsAdmin, ]
    authentication_classes = [TokenAuthentication, ]

    def get_queryset(self):
        return ProfileSkill.objects.filter(profile=self.kwargs['profile_pk'])


class ProfileEducationViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated & IsProfileOwner | IsAdmin, ]
    authentication_classes = [TokenAuthentication, ]

    def get_queryset(self):
        return ProfileEducation.objects.filter(profile=self.kwargs['profile_pk'])


class ProfileExperienceViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated & IsProfileOwner | IsAdmin, ]
    authentication_classes = [TokenAuthentication, ]

    def get_queryset(self):
        return ProfileExperience.objects.filter(profile=self.kwargs['profile_pk'])


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated & IsOwner | IsAdmin | ReadOnly, ]
    authentication_classes = [TokenAuthentication, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated & IsCompany & IsCompanyOwner | IsAdmin | ReadOnly, ]
    authentication_classes = [TokenAuthentication, ]

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer


class TaskUserViewSet(viewsets.ModelViewSet):
    queryset = TaskUser.objects.all()
    serializer_class = TaskUserSerializer
    permission_classes = [IsAuthenticated & CreateOnly | IsAdmin, ]
    authentication_classes = [TokenAuthentication, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostSkillViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated & IsCompany & IsPostOwner | IsAdmin | ReadOnly, ]
    authentication_classes = [TokenAuthentication, ]

    def get_queryset(self):
        return PostSkill.objects.filter(profile=self.kwargs['post_pk'])


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated & IsCompany & IsCompanyOwner | IsAdmin | ReadOnly, ]
    authentication_classes = [TokenAuthentication, ]

    def perform_create(self, serializer):
        company = get_object_or_404(Company, user=self.request.user)
        serializer.save(company=company)


class SubmissionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                        mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
