# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20140908_0306'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='duration',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
