from django.db import models
from django.contrib.auth.models import User
import jsonfield


class Story(models.Model):
    title = models.CharField(max_length=256)
    created_by = models.ForeignKey(User)
    root = models.ForeignKey('StoryNode', related_name='+', null=True)


class StoryNode(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    parent = models.ForeignKey('StoryNode', null=True)
    story = models.ForeignKey(Story)
    stars = models.IntegerField(default=0)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
