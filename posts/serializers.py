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
    skill_ = serializers.CharField(write_only=True)

    class Meta:
        model = ProfileSkill
        exclude = ["profile", "id"]
        depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response = response.pop("skill")
        return response

    @staticmethod
    def create_profile(instance, validated_data):
        skills = [skill["skill_"] for skill in validated_data]
        for skill in skills:
            skill = Skill.objects.get(name=skill)
            ProfileSkill.objects.create(profile=instance, skill=skill)

    @staticmethod
    def update_profile(instance, validated_data):
        skills = [skill["skill_"] for skill in validated_data]
        existing_skills = [skill.skill.name for skill in ProfileSkill.objects.filter(
            profile_id=instance.id).all()]
        for existing in existing_skills:
            if existing not in validated_data:
                ProfileSkill.objects.filter(profile=instance, skill__name=existing).delete()
        for skill in skills:
            if skill not in existing_skills:
                skill = Skill.objects.get(name=skill)
                ProfileSkill.objects.create(profile=instance, skill=skill)


class ProfileEducationSerializer(serializers.ModelSerializer):
    institution_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProfileEducation
        exclude = ["profile", ]
        depth = 1

    @staticmethod
    def create_profile(instance, validated_data):
        for education in validated_data:
            institution = Institution.objects.get(id=education["institution_id"])
            ProfileEducation.objects.create(
                profile=instance,
                institution=institution,
                start_date=education["start_date"],
                end_date=education["end_date"]
            )

    @staticmethod
    def update_profile(instance, validated_data):
        institutions = [data["institution_id"] for data in validated_data]
        existing_institutions = [data.institution.id for data in ProfileEducation.objects.filter(
            profile_id=instance.id).all()]
        for existing in existing_institutions:
            if existing not in institutions:
                ProfileEducation.objects.filter(profile=instance, institution_id=existing).delete()
        for data in validated_data:
            if data["institution_id"] not in existing_institutions:
                institution = Institution.objects.get(id=data["institution_id"])
                ProfileEducation.objects.create(
                    profile=instance,
                    institution=institution,
                    start_date=data["start_date"],
                    end_date=data["end_date"]
                )
            else:
                ProfileEducation.objects.filter(profile=instance, institution_id=existing).update(
                    start_date=data["start_date"],
                    end_date=data["end_date"]
                )


class ProfileExperienceSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProfileExperience
        fields = "__all__"
        read_only_fields = ('profile',)

    @staticmethod
    def create_profile(instance, validated_data):
        for experience in validated_data:
            company = Company.objects.get(id=experience["company_id"])
            ProfileExperience.objects.create(
                profile=instance,
                company=company,
                start_date=experience["start_date"],
                end_date=experience["end_date"],
                description=experience["description"]
            )

    @staticmethod
    def update_profile(instance, validated_data):
        companies = [data["company_id"] for data in validated_data]
        existing_companies = [data.company.id for data in ProfileExperience.objects.filter(
            profile_id=instance.id).all()]
        for existing in existing_companies:
            if existing not in companies:
                ProfileExperience.objects.filter(profile=instance, company_id=existing).delete()
        for data in validated_data:
            if data["company_id"] not in existing_companies:
                company = Company.objects.get(id=data["company_id"])
                ProfileExperience.objects.create(
                    profile=instance,
                    company=company,
                    start_date=data["start_date"],
                    end_date=data["end_date"],
                    description=data["description"]
                )
            else:
                ProfileExperience.objects.filter(profile=instance, company_id=existing).update(
                    start_date=data["start_date"],
                    end_date=data["end_date"],
                    description=data["description"]
                )


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
          {"name":"python"}
      ],
      "education": [
          {"institution_id":1,"start_date":"2015-02-11", "end_date":"2015-02-11"}
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

        ProfileSkillSerializer.create_profile(profile, skills)
        ProfileEducationSerializer.create_profile(profile, education)
        ProfileExperienceSerializer.create_profile(profile, experience)
        return profile

    def update(self, instance, validated_data):
        skills = validated_data.pop('skills') if "skills" in validated_data else []
        education = validated_data.pop('education') if "education" in validated_data else []
        experience = validated_data.pop('experiences') if "experiences" in validated_data else []

        ProfileSkillSerializer.update_profile(instance, skills)
        ProfileEducationSerializer.update_profile(instance, education)
        ProfileExperienceSerializer.update_profile(instance, experience)

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
