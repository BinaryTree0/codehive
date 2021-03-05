from django.db import models

from custom.models import CustomUser


class Post(models.Model):
    author = models.ForeignKey(CustomUser, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    description = models.TextField()
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)

# The storage thing will be complicated, need to look at best practices


class Task(models.Model):
    class Difficulties(models.IntegerChoices):
        EASY = 0, 'Easy'
        INTERMEDIATE = 1, 'Intermediate'
        HARD = 2, 'Hard'
    post = models.ForeignKey(Post, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(choices=Difficulties.choices, max_length=12)
    files = models.FileField(upload_to='tasks/')
    time_limit = models.DateTimeField()


class Result(models.Model):
    author = models.ForeignKey(CustomUser, related_name='results', on_delete=models.CASCADE)
    files = models.FileField(upload_to='results/')
    description = models.TextField()
