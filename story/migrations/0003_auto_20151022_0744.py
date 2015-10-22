# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0002_story_root'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='root',
            field=models.ForeignKey(related_name='+', to='story.StoryNode', null=True),
        ),
    ]
