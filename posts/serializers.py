from rest_framework import serializers

from .models import Institution, Profile, ProfileSkill, \
    ProfileEducation, ProfileExperience, Post, Task, Company, Submission


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = "__all__"


class ProfileSkill(serializers.ModelSerializer):
    class Meta:
        model = ProfileSkill
        fileds = "__all__"


class ProfileEducation(serializers.ModelSerializer):
    class Meta:
        model = ProfileEducation
        fileds = "__all__"


class ProfileExperience(serializers.ModelSerializer):
    class Meta:
        model = ProfileExperience
        fileds = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('author',)
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


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
