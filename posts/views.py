from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

import django_filters.rest_framework

from .models import (Company, Institution, Post, Profile,
                     ProfileEducation, ProfileExperience, ProfileSkill, Skill,
                     Submission, Task, TaskUser, TestFileUpload)
from .permissions import (CreateOnly, IsAdmin, IsAuthenticated, IsCompany,
                          IsTaskOwner, IsOwner, IsPostOwner, IsProfileOwner,
                          ReadOnly)
from .serializers import (CompanySerializer, InstitutionSerializer,
                          PostSerializer, TestFileUploadSerializer,
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
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name', 'id']

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdmin | ReadOnly, ]


class ProfileSkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated & IsProfileOwner | IsAdmin, ]
    authentication_classes = [TokenAuthentication, ]
    serializer_class = ProfileSkillSerializer

    def get_queryset(self):
        return ProfileSkill.objects.filter(profile=self.kwargs['profile_pk'])

    def perform_create(self, serializer):
        profile = Profile.objects.get(id=self.kwargs['profile_pk'])
        skill = Skill.objects.get(id=serializer.validated_data["skill_id"])
        serializer.save(profile=profile)
        serializer.save(skill=skill)


class ProfileEducationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated & IsProfileOwner | IsAdmin, ]
    authentication_classes = [TokenAuthentication, ]
    serializer_class = ProfileEducationSerializer

    def get_queryset(self):
        return ProfileEducation.objects.filter(profile=self.kwargs['profile_pk'])

    def perform_create(self, serializer):
        profile = Profile.objects.get(id=self.kwargs['profile_pk'])
        institution = Institution.objects.get(id=serializer.validated_data["institution_id"])
        serializer.save(profile=profile)
        serializer.save(institution=institution)


class ProfileExperienceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated & IsProfileOwner | IsAdmin, ]
    authentication_classes = [TokenAuthentication, ]
    serializer_class = ProfileExperienceSerializer

    def get_queryset(self):
        return ProfileExperience.objects.filter(profile=self.kwargs['profile_pk'])

    def perform_create(self, serializer):
        profile = Profile.objects.get(id=self.kwargs['profile_pk'])
        company = Company.objects.get(id=serializer.validated_data["company_id"])
        serializer.save(profile=profile)
        serializer.save(company=company)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated & IsOwner | IsAdmin | ReadOnly, ]
    authentication_classes = [TokenAuthentication, ]

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['user_id']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['post', ]

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated & IsCompany & IsTaskOwner | IsAdmin | ReadOnly, ]
    authentication_classes = [TokenAuthentication, ]


class TaskUserViewSet(viewsets.ModelViewSet):
    queryset = TaskUser.objects.all()
    serializer_class = TaskUserSerializer
    permission_classes = [IsAuthenticated & CreateOnly | IsAdmin, ]
    authentication_classes = [TokenAuthentication, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated & IsCompany & IsPostOwner | IsAdmin | ReadOnly, ]
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


class TestFileUploadViewSet(viewsets.ModelViewSet):
    queryset = TestFileUpload.objects.all()
    serializer_class = TestFileUploadSerializer

    def create(self, request):
        print(request["data"])
        pass
