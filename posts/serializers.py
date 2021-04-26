from rest_framework import serializers

from custom.models import CustomUser
from .models import Institution, Profile, ProfileSkill, Skill,\
    ProfileEducation, ProfileExperience, Post, Task, Company, Submission, PostUser, PostSkill


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


class ProfileSerializer(NestedModelSerializer):
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

    def get_nested_arguments(self):
        return [
            {"field": "skills", "id": "skill_id", "class": ProfileSkill},
            {"field": "education", "id": "institution_id", "class": ProfileEducation},
            {"field": "experiences", "id": "company_id", "class": ProfileExperience}
        ]

    def get_model_arguments(self):
        return {"field_name": "profile", "model": Profile}

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
        exclude = ["post", ]


class PostSkillSerializer(serializers.ModelSerializer):
    skill_id = serializers.CharField(write_only=True)

    class Meta:
        model = PostSkill
        exclude = ["post", "skill"]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response = response.pop("skill")
        return response


class PostSerializer(NestedModelSerializer):
    tasks = TaskSerializer(many=True, required=False)
    skills = PostSkillSerializer(many=True, required=False)
    """
    {
      "skills": [
          {"skill_id": 1}
      ],
      "tasks": [
          {"title": "Hello"},
          {"title": "Lets gooo"}
      ],
      "position": "a"
    }
    """
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('company',)

    def get_nested_arguments(self):
        return [
            {"field": "skills", "id": "skill_id", "class": PostSkill},
            {"field": "tasks", "id": "title", "class": Task}
        ]

    def get_model_arguments(self):
        return {"field_name": "post", "model": Post}


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["post", "title"]


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
