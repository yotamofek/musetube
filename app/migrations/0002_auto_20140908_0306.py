# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='encode_task',
            field=models.CharField(null=True, max_length=36),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='upload_task',
            field=models.CharField(null=True, max_length=36),
            preserve_default=True,
        ),
    ]
