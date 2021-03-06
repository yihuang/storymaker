from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Story(models.Model):
    title = models.CharField(max_length=256)
    created_by = models.ForeignKey(User)
    root = models.ForeignKey('StoryNode', related_name='+', null=True)

    def get_absolute_url(self):
        return reverse('story:story', kwargs={'id': self.id})


class StoryNode(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    parent = models.ForeignKey('StoryNode', null=True)
    story = models.ForeignKey(Story)
    stars = models.IntegerField(default=0)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('story:node', kwargs={'id': self.id})
