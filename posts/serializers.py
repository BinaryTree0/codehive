from rest_framework import serializers

from custom.models import CustomUser
from rest_framework.parsers import MultiPartParser
from .models import (Company, Institution, Post, Profile,
                     ProfileEducation, ProfileExperience, ProfileSkill, Skill,
                     Submission, Task, TaskUser, TestFileUpload)


class NestedModelSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        arguments = self.get_nested_arguments()
        for item in arguments:
            item["data"] = validated_data.pop(
                item["field"]) if item["field"] in validated_data else []

        model_arguments = self.get_model_arguments()
        model, field_name = model_arguments["model"], model_arguments["field_name"]
        instance = model.objects.create(**validated_data)
        model_data = {field_name: instance}

        for item in arguments:
            for data in item["data"]:
                item["class"].objects.create(**model_data, **data)
        return instance

    def update(self, instance, validated_data):
        model_arguments = self.get_model_arguments()
        model, field_name = model_arguments["model"], model_arguments["field_name"]
        model_data = {field_name: instance}

        arguments = self.get_nested_arguments()
        for item in arguments:
            item["data"] = validated_data.pop(
                item["field"]) if item["field"] in validated_data else []
            for data in item["data"]:
                data = {**model_data, **data}
                filter_ = {}
                for field in [item["id"], field_name]:
                    filter_[field] = data.pop(field)
                item["class"].objects.update_or_create(**filter_, defaults=data)

        model.objects.filter(id=instance.id).update(**validated_data)
        return instance


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ("user",)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProfileSkillSerializer(serializers.ModelSerializer):
    skill_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProfileSkill
        exclude = ["profile", "id"]
        depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response = response.pop("skill")
        return response


class ProfileEducationSerializer(serializers.ModelSerializer):
    institution_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProfileEducation
        exclude = ["profile", ]
        depth = 1


class ProfileExperienceSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProfileExperience
        exclude = ['profile', ]
        depth = 1


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "is_company"]


class ProfileSerializer(serializers.ModelSerializer):
    user = ProfileUserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        depth = 1


class TaskUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskUser
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class TaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ["post", "title"]


class PostSerializer(serializers.ModelSerializer):
    parser_classes = [MultiPartParser]

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('company',)
        depth = 1


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"


class TestFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestFileUpload
        fields = "__all__"
