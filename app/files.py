#!/usr/bin/python3
import os
import random
from tempfile import NamedTemporaryFile

from boto import connect_s3
import boto

from django.conf import settings
from io import BytesIO
import io

s3 = connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
bucket = s3.get_bucket(settings.S3_BUCKET)

def _create_random_key(bucket, path, suffix=''):
    charset = 'abcdef1234567890'

    key = None
    while not key:
        name = os.path.join(path, ''.join(random.choice(charset) for _ in range(8)) + suffix)
        try:
            return bucket.new_key(name)
        except:
            continue


def save_file_to_s3(f, suffix='', cb=None):
    global bucket

    if not suffix:
        suffix = _get_ext(f.name)

    key = _create_random_key(bucket, '', suffix=suffix)

    key.set_contents_from_file(f, cb=cb)
    return key


def save_filename_to_s3(fname, **kwargs):
    return save_file_to_s3(open(fname, 'rb'), **kwargs)


def get_key(name):
    return bucket.get_key(name)


def download_key_to_temp(key):
    key = get_key(key)

    temp_file = NamedTemporaryFile(suffix=_get_ext(key.name))
    key.get_contents_to_file(temp_file)

    return temp_file

def download_key_to_stream(key):
    stream = BytesIO()
    get_key(key).get_contents_to_file(stream)
    stream.seek(0)

    return stream


def _get_ext(file_name):
    return os.path.splitext(file_name)[1]


def save_file_to_temp(f):
    temp_file = NamedTemporaryFile(suffix=_get_ext(f.name), delete=False)
    temp_file.write(f.read())

    return os.path.abspath(temp_file.name)