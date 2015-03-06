from math import floor
import os
from tempfile import NamedTemporaryFile
from PIL import Image
from django.conf import settings
from subprocess import Popen, PIPE
from app import files
from app.ffmpeg import ffmpeg_stderr_reader, reader
from app.models import Song
from app.youtube import upload_to_youtube
from musetube.celery import app as celery_app


@celery_app.task
def upload_to_s3(f):
    return


@celery_app.task
def encode_video(song_id, crop_y):
    song = Song.objects.get(pk=song_id)
    image = Image.open(files.download_key_to_stream(song.image))

    crop_y = crop_y * image.size[0] / settings.THUMBNAIL_WIDTH
    crop_dimensions = (0, floor(crop_y), image.size[0], floor(crop_y + (image.size[0] / 16 * 9)))

    _, extension = os.path.splitext(song.image)
    cropped_image = NamedTemporaryFile(suffix=extension)

    cropped = image.crop(crop_dimensions)
    cropped.thumbnail((1280, 720), Image.ANTIALIAS)
    cropped.save(cropped_image, format=image.format)

    audio = files.download_key_to_temp(song.audio)
    video = NamedTemporaryFile(suffix='.mp4')

    queue = song.encode_task_queue

    with cropped_image, audio:
        command = 'ffmpeg -y -loop 1 -i {image} -i {audio} -c:a libfdk_aac -b:a 320k ' \
                  '-c:v libx264 -b:v 5000k -s hd720 -pix_fmt yuv420p -preset faster -shortest -r 30 ' \
                  '-f mp4 -frag_duration 3600 {video}' \
            .format(image=cropped_image.name, audio=audio.name, video=video.name)

        process = Popen(command, shell=True, stderr=PIPE)

        for params in ffmpeg_stderr_reader(process.stderr):
            params['status'] = 'encoding'
            print(params)
            queue.put(params)

    def upload_progress_callback(total_size, completed):
        queue.put({'status': 'uploading', 'completed': 100 * total_size / completed})

    with video:
        queue.put({'status': 'uploading'})
        youtube_id = upload_to_youtube(song, video, upload_progress_callback)

    queue.put({'status': 'uploaded', 'id': youtube_id})
