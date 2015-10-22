# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='root',
            field=models.ForeignKey(related_name='+', default=1, to='story.StoryNode'),
            preserve_default=False,
        ),
    ]
