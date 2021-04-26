from rest_framework import serializers

from custom.models import CustomUser
from .models import Institution, Profile, ProfileSkill, Skill,\
    ProfileEducation, ProfileExperience, Post, Task, Company, Submission, PostUser, PostSkill


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

    def get_nested_arguments(self):
        return [
            {"field": "skills", "id": "skill_id", "class": ProfileSkill},
            {"field": "education", "id": "institution_id", "class": ProfileEducation},
            {"field": "experiences", "id": "company_id", "class": ProfileExperience}
        ]

    def get_model_arguments(self):
        return {"field_name": "profile", "model": Profile}

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
            create_nested(model=item["class"], validated_data=item["data"], **model_data)
        return instance

    def update(self, instance, validated_data):
        model_arguments = self.get_model_arguments()
        model, field_name = model_arguments["model"], model_arguments["field_name"]
        model_data = {field_name: instance}

        arguments = self.get_nested_arguments()
        for item in arguments:
            data = validated_data.pop(item["field"]) if item["field"] in validated_data else []
            update_profile(model=item["class"], validated_data=data,
                           unique=[item["id"], "profile"], **model_data)

        model.objects.filter(id=instance.id).update(**validated_data)
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


class PostSkillSerializer(serializers.ModelSerializer):
    skill_id = serializers.CharField(write_only=True)

    class Meta:
        model = PostSkill
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response = response.pop("skill")
        return response


class PostSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, required=True)
    skills = PostSkillSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('company',)

    def create(self, validated_data):
        tasks = validated_data.pop('tasks') if "tasks" in validated_data else []
        skills = validated_data.pop('skills') if "skills" in validated_data else []

        post = Post.objects.create(**validated_data)

        PostUser.objects.create(post=post, user=validated_data["user"])
        create_nested(model=Task, validated_data=tasks, post=post)
        create_nested(model=PostSkill, validated_data=skills, post=post)
        return profile

    def update(self, instance, validated_data):
        tasks = validated_data.pop('tasks') if "tasks" in validated_data else []
        skills = validated_data.pop('skills') if "skills" in validated_data else []

        update_profile(model=Task, validated_data=tasks,
                       unique=["post", "title"], post=instance)
        update_profile(model=PostSkill, validated_data=skills,
                       unique=["skill_id", "profile"], post=instance)

        Profile.objects.filter(id=instance.id).update(**validated_data)
        return instance


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["post", "title", "difficulty", "time_limit"]


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
