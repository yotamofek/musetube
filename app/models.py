from django.conf import settings
from django.db import models
from app.queues import create_queue


class Song(models.Model):
    image = models.CharField(max_length=20)
    thumbnail = models.CharField(max_length=20)

    audio = models.CharField(max_length=20)
    duration = models.FloatField(null=True)

    name = models.CharField(max_length=250)

    encode_task = models.CharField(max_length=36, null=True)
    upload_task = models.CharField(max_length=36, null=True)

    google_access_token = models.TextField(null=True)

    @property
    def encode_task_queue(self):
        name = ':'.join(('encode', str(self.pk)))

        conn = settings.KOMBU_CONN
        return conn.SimpleBuffer(name)
