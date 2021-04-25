from rest_framework import serializers

from custom.models import CustomUser
from .models import Institution, Profile, ProfileSkill, Skill,\
    ProfileEducation, ProfileExperience, Post, Task, Company, Submission


def create_nested(model, validated_data, **kwargs):
    for data in validated_data:
        model.objects.create(**kwargs, **data)


def update_profile(model, validated_data, unique, **kwargs):
    for data in validated_data:
        data = {**kwargs, **data}
        filter_ = {}
        for field in unique:
            filter_[field] = data.pop(field)
        model.objects.update_or_create(**filter_, defaults=data)


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProfileSkillSerializer(serializers.ModelSerializer):
    skill_id = serializers.CharField(write_only=True)

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
        fields = "__all__"
        read_only_fields = ('profile',)


class StringListField(serializers.ListField):
    child = serializers.CharField(max_length=100)


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "is_company"]


class ProfileSerializer(serializers.ModelSerializer):
    skills = ProfileSkillSerializer(many=True, required=False)
    education = ProfileEducationSerializer(many=True, required=False)
    experiences = ProfileExperienceSerializer(many=True, required=False)
    user = ProfileUserSerializer(read_only=True)

    """
{
  "skills": [
      {"skill_id": 1}
  ],
  "education": [
      {"institution_id":1,"title": "Hello","start_date":"2015-02-11", "end_date":"2015-02-11"}
  ],
  "experiences": [
      {"company_id":1,"start_date":"2015-02-11", "end_date":"2017-02-11", "description":"Hello world"}
  ],
  "first_name": "a",
  "last_name": "a"
}
    """

    def create(self, validated_data):
        skills = validated_data.pop('skills') if "skills" in validated_data else []
        education = validated_data.pop('education') if "education" in validated_data else []
        experience = validated_data.pop('experiences') if "experiences" in validated_data else []

        profile = Profile.objects.create(**validated_data)

        create_nested(model=ProfileSkill, validated_data=skills, profile=profile)
        create_nested(model=ProfileEducation, validated_data=education, profile=profile)
        create_nested(model=ProfileExperience, validated_data=experience, profile=profile)
        return profile

    def update(self, instance, validated_data):
        skills = validated_data.pop('skills') if "skills" in validated_data else []
        education = validated_data.pop('education') if "education" in validated_data else []
        experience = validated_data.pop('experiences') if "experiences" in validated_data else []

        update_profile(model=ProfileSkill, validated_data=skills,
                       unique=["skill_id", "profile"], profile=instance)
        update_profile(model=ProfileEducation, validated_data=education,
                       unique=["institution_id", "profile"], profile=instance)
        update_profile(model=ProfileExperience, validated_data=experience,
                       unique=["company_id", "profile"], profile=instance)

        Profile.objects.filter(id=instance.id).update(**validated_data)
        return instance

    class Meta:
        model = Profile
        fields = "__all__"
        depth = 1


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ("user",)


class CompanyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["image", "name"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('company',)


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["post", "title", "difficulty", "time_limit"]


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
