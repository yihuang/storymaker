from django.contrib import admin
from .models import Story, StoryNode


@admin.register(Story, StoryNode)
class DefaultAdmin(admin.ModelAdmin):
    pass
