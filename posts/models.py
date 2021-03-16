from django.db import models
from django.template.defaultfilters import slugify
from custom.models import CustomUser


def get_upload_post_path(instance, filename):
    post_media_url = slugify(str(instance.author.id))+"/" + \
        slugify(str(instance.title))+"/"+slugify(str(instance.created))
    return 'posts/' + post_media_url + "/" + filename


class Post(models.Model):
    author = models.ForeignKey(CustomUser, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    summary = models.TextField()
    description = models.TextField()
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=get_upload_post_path)


def get_upload_task_path(instance, filename):
    return 'tasks/' + str(instance.post.id) + "/" + slugify(str(instance.title)) +\
        "/"+slugify(str(instance.created))+"/"+filename


class Task(models.Model):
    class Difficulties(models.IntegerChoices):
        EASY = 0, 'Easy'
        INTERMEDIATE = 1, 'Intermediate'
        HARD = 2, 'Hard'
    post = models.ForeignKey(Post, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(choices=Difficulties.choices, max_length=12)
    files = models.FileField(upload_to=get_upload_task_path)
    time_limit = models.DateTimeField()
    created = models.DateTimeField()


def get_upload_result_path(instance, filename):
    return 'results/'+str(instance.task.post.id)+"/"+str(instance.task.id)+"/"+str(user.id)


class Result(models.Model):
    author = models.ForeignKey(CustomUser, related_name='results', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name="results", on_delete=models.CASCADE)
    description = models.TextField()
    files = models.FileField(upload_to=get_upload_result_path)
