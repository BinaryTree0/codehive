from django.db import models
from django.template.defaultfilters import slugify
from custom.models import CustomUser


def get_upload_institution_path(instance, filename):
    return 'image/' + slugify(instance.location) + "/"+slugify(instance.name)+"/institution." + filename.split(".")[-1]


class Institution(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_upload_institution_path)

    class Meta:
        unique_together = ('name', 'location')


def get_upload_user_image_path(instance, filename):
    return 'image/' + slugify(instance.user.id) + "/user." + filename.split(".")[-1]


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_user_image_path)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    about = models.TextField()
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    github = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)
    website = model.CharField(max_length=100)


class ProfileSkill:
    profile = models.ForeignKey(Profile, related_name='skill', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class ProfileEducation:
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()


class ProfileExperience:
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()


class Company(models.Model):
    user = models.OneToOneField(CustomUser, related_name='company', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_user_image_path)
    name = models.CharField(max_length=200)
    size = models.IntegerField()
    founded = models.DateField()
    address = models.CharField(max_length=200)
    description = models.TextField()
    facebook = models.CharField(max_length=200)
    linkedin = models.CharField(max_length=200)
    twitter = models.CharField(max_length=200)
    website = models.CharField(max_length=200)


def get_upload_post_path(instance, filename):
    return 'posts/' + slugify(str(instance.author.id))+"/" + slugify(str(instance.title))\
        + "."+filename.split(".")[-1]


class Post(models.Model):
    company = models.ForeignKey(Company, related_name='posts', on_delete=models.CASCADE)
    position = models.CharField(max_length=200)
    salary_low = models.IntegerField()
    salary_high = models.IntegerField()
    currency = models.CharField(max_length=40)
    position = models.CharField(max_length=200)
    experience = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    post_description = models.TextField()
    post_role_description = models.TextField()
    tasks_summary = models.TextField()
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    ends = models.DateTimeField()


class PostSkill(models.Model):
    post = models.ForeignKey(Post, related_name="skills", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class PostUser(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)


def get_upload_task_path(instance, filename):
    return 'tasks/' + str(instance.post.id) + "/" + slugify(str(instance.title))+"/"+filename


class Task(models.Model):
    class Difficulties(models.IntegerChoices):
        EASY = 0, 'Easy'
        INTERMEDIATE = 1, 'Intermediate'
        HARD = 2, 'Hard'
    post = models.ForeignKey(Post, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    code = models.FileField(upload_to=get_upload_task_path)
    test = models.FileField(upload_to=get_upload_task_path)
    requirements = models.FileField(upload_to=get_upload_task_path)
    tags = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('post_id', 'title',)


class TaskTag(models.Model):
    task = models.ForeignKey(Task, related_name='tags', on_delete=models.CASCADE)
    tag = models.CharField(max_length=100)


def get_upload_submission_path(instance, filename):
    return 'submissions/'+str(instance.task.post.id)+"/"+str(instance.task.id)+"/"+str(instance.author.id) + "."+filename.split(".")[-1]


class Submission(models.Model):
    author = models.ForeignKey(CustomUser, related_name='submissions', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name="submissions", on_delete=models.CASCADE)
    code = models.TextField()

    class Meta:
        unique_together = ('author_id', 'task_id',)
