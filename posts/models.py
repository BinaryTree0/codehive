from django.db import models
from django.template.defaultfilters import slugify

from custom.models import CustomUser


def get_upload_user_image_path(instance, filename):
    return 'image/' + slugify(instance.user.id) + "/user." + filename.split(".")[-1]


class Company(models.Model):
    user = models.OneToOneField(CustomUser, related_name='company', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_user_image_path, null=True, blank=True)
    name = models.CharField(max_length=200)
    size = models.IntegerField()
    founded = models.DateField()
    address = models.CharField(max_length=200)
    description = models.TextField()
    facebook = models.CharField(max_length=200, null=True, blank=True)
    linkedin = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)

    @classmethod
    def get_default_pk(cls):
        company, created = cls.objects.get_or_create(
            user=1,
            defaults=dict(
                name="default",
                size=0,
                founded="default",
                address="default",
                description="default"
            )
        )
        return company.pk


def get_upload_institution_path(instance, filename):
    return 'image/' + slugify(instance.location) + "/"+slugify(instance.name)+"/institution." + filename.split(".")[-1]


class Institution(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_upload_institution_path)

    @classmethod
    def get_default_pk(cls):
        institution, created = cls.objects.get_or_create(
            name='default name',
            defaults=dict(description='default description')
        )
        return institution.pk

    class Meta:
        unique_together = ('name', 'location')


class Skill(models.Model):
    name = models.CharField(max_length=100)
    type = models.BooleanField()


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, null=True, blank=True,
                                related_name='profiles', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_user_image_path, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    github = models.CharField(max_length=100, null=True, blank=True)
    linkedin = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)


class ProfileSkill(models.Model):
    profile = models.ForeignKey(Profile, related_name='skills', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, related_name='profile_skills', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('skill_id', 'profile',)


class ProfileEducation(models.Model):
    profile = models.ForeignKey(Profile, related_name='education', on_delete=models.CASCADE)
    institution = models.ForeignKey(
        Institution, default=Institution.get_default_pk, on_delete=models.SET_DEFAULT)
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()


class ProfileExperience(models.Model):
    profile = models.ForeignKey(Profile, related_name="experiences", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name="experiences",
                                default=Company.get_default_pk, on_delete=models.SET_DEFAULT)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()


def get_upload_post_path(instance, filename):
    return 'posts/' + slugify(str(instance.author.id))+"/" + slugify(str(instance.title))
    + "."+filename.split(".")[-1]


class Post(models.Model):
    company = models.ForeignKey(Company, related_name='posts', on_delete=models.CASCADE)
    position = models.CharField(max_length=200, null=True, blank=True)
    experience = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)


def get_upload_task_path(instance, filename):
    return 'tasks/' + str(instance.post.id) + "/" + slugify(str(instance.title))+"/"+filename


class Task(models.Model):
    post = models.ForeignKey(Post, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    language = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    code = models.FileField(upload_to=get_upload_task_path, null=True, blank=True)
    test = models.FileField(upload_to=get_upload_task_path, null=True, blank=True)
    requirements = models.FileField(upload_to=get_upload_task_path, null=True, blank=True)
    created = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = ('post_id', 'title',)


class TaskUser(models.Model):
    user = models.ForeignKey(CustomUser, related_name='task_user', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='task_user', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True, null=True, blank=True)


def get_upload_submission_path(instance, filename):
    return 'submissions/'+str(instance.task.post.id)+"/"+str(instance.task.id)+"/"+str(instance.author.id) + "."+filename.split(".")[-1]


class Submission(models.Model):
    user = models.ForeignKey(CustomUser, related_name='submissions', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name="submissions", on_delete=models.CASCADE)
    code = models.TextField()

    class Meta:
        unique_together = ('user_id', 'task_id',)


def get_upload_test_path(instance, filename):
    return 'test/'+filename


class TestFileUpload(models.Model):
    code = models.FileField(upload_to=get_upload_test_path, null=True, blank=True)
