# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20141030_0644'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='google_access_token',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
