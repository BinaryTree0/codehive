from rest_framework import serializers

from custom.models import CustomUser
from .models import Institution, Profile, ProfileSkill, Skill,\
    ProfileEducation, ProfileExperience, Post, Task, Company, Submission


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProfileSkillSerializer(serializers.ModelSerializer):
    profile_skill = serializers.CharField(write_only=True)

    class Meta:
        model = ProfileSkill
        exclude = ["profile", "id"]
        depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['profile_skill'] = response.pop("skill")
        return response

    @staticmethod
    def create_profile(instance, validated_data):
        skills = [skill["profile_skill"] for skill in validated_data]
        for skill in skills:
            skill = Skill.objects.get(name=skill)
            ProfileSkill.objects.create(profile=instance, skill=skill)

    @staticmethod
    def update_profile(instance, validated_data):
        skills = [skill["profile_skill"] for skill in validated_data]
        existing_skills = [skill.skill.name for skill in ProfileSkill.objects.filter(
            profile_id=instance.id).all()]
        for existing in existing_skills:
            if existing not in validated_data:
                ProfileSkill.objects.filter(skill__name=existing).delete()
        for skill in skills:
            if skill not in existing_skills:
                skill = Skill.objects.get(name=skill)
                ProfileSkill.objects.create(profile=instance, skill=skill)


class ProfileEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileEducation
        fields = "__all__"
        read_only_fields = ('profile',)


class ProfileExperienceSerializer(serializers.ModelSerializer):
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
    profile_skills = ProfileSkillSerializer(many=True)
    user = ProfileUserSerializer(read_only=True)

    """
{
  "profile_skills": [
      {"profile_skill":"python"},
      {"profile_skill":"java"}
  ],
  "first_name": "a",
  "last_name": "a"
}
    """

    def create(self, validated_data):
        skills = validated_data.pop('profile_skills') if "profile_skills" in validated_data else []
        profile = Profile.objects.create(**validated_data)
        ProfileSkillSerializer.create_profile(profile, skills)
        return profile

    def update(self, instance, validated_data):
        skills = validated_data.pop('profile_skills') if "profile_skills" in validated_data else []
        ProfileSkillSerializer.update_profile(instance, skills)

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


class PostSerializer(serializers.ModelSerializer):
    company = CompanyPostSerializer()

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('company',)
        extra_kwargs = {'image': {'max_length': 200, 'allow_empty_file': False, 'use_url': True}}


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
