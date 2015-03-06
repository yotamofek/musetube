from io import BytesIO
import json
from tempfile import NamedTemporaryFile
import os.path
from PIL import Image
import audioread

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from app import files



def main(request):
    song = request.song

    return render(request, 'main.html', {
        'thumbnail': files.get_key(song.thumbnail).generate_url(100) if song.thumbnail else None,
        'audio': files.get_key(song.audio).generate_url(100) if song.audio else None,
        'google_redirect_uri': request.build_absolute_uri(reverse(google_auth)),
    })


def _create_thumbnail(f):
    image = Image.open(f)
    image.thumbnail((settings.THUMBNAIL_WIDTH, settings.THUMBNAIL_WIDTH), Image.ANTIALIAS)

    thumbnail = BytesIO()
    image.save(thumbnail, format='PNG')
    thumbnail.seek(0)

    key = files.save_file_to_s3(thumbnail, '.png')

    return key


def upload_image(request):
    song = request.song
    image = request.FILES['image']

    song.image = files.save_file_to_s3(image).name
    image.seek(0)

    thumbnail = _create_thumbnail(image)
    song.thumbnail = thumbnail.name
    song.save()

    return HttpResponse(thumbnail.generate_url(100))


def upload_audio(request):
    song = request.song
    audio = request.FILES['audio']
    song.name = os.path.splitext(audio.name)[0]

    with NamedTemporaryFile() as temp_audio:
        temp_audio.write(audio.read())
        audio.seek(0)
        song.duration = audioread.audio_open(temp_audio.name).duration

    audio = files.save_file_to_s3(audio)
    song.audio = audio.name
    song.save()

    return HttpResponse(audio.generate_url(100))


def submit(request):
    from app.tasks import encode_video

    encode_video.delay(request.song.pk, int(request.GET['crop-y']))

    return HttpResponse('ok')


def parse_ffmpeg_time(time):
    hours, minutes, seconds = map(float, time.split(':'))

    return seconds + (minutes * 60) + (hours * 60 * 60)


def format_task_result(result, song):
    if result.get('status', None) == 'encoding':
        if result.get('completed', False):
            completion = 100
        else:
            completion = 100 * parse_ffmpeg_time(result['time']) / song.duration

        return {'status': 'encoding', 'completion': int(completion)}
    else:
        return result


class MessageManager():
    def __init__(self, message):
        self._message = message

    def __enter__(self):
        return self._message

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._message.ack()


def poll_task(request):
    queue = request.song.encode_task_queue

    try:
        message = queue.get(block=False)
        result = message.payload if message else None
    except queue.Empty:
        result = None

    if result:
        return HttpResponse(json.dumps(format_task_result(result, request.song)), content_type='application/json')
    else:
        return HttpResponse(status=204)


def google_auth(request):
    request.song.google_access_token = requests.post('https://accounts.google.com/o/oauth2/token', data={
        'code': request.GET['code'],
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': request.build_absolute_uri(reverse(google_auth)),
        'grant_type': 'authorization_code'
    }).json()['access_token']
    request.song.save()

    return redirect(reverse(main))