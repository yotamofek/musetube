# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_song_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='duration',
            field=models.FloatField(null=True),
        ),
    ]
