import apiclient.discovery
import apiclient.errors
import apiclient.http
from googleapiclient.http import MediaFileUpload
import httplib2
from oauth2client.client import AccessTokenCredentials


def upload_to_youtube(song, video, progress_callback):
    credentials = AccessTokenCredentials(song.google_access_token, 'musetube/0.1')

    youtube = apiclient.discovery.build('youtube', 'v3', http=credentials.authorize(httplib2.Http()))

    body = {
        'snippet': {
            'title': song.name,
            'description': '',
        },
        'status': {
            'privacyStatus': 'private',
        }
    }

    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(video.name, chunksize=1024 * 1024, resumable=True),
    )

    response = None
    while not response:
        status, response = insert_request.next_chunk()

        if not response and status:
            progress_callback(status.total_size, status.resumable_progress)

    if 'id' in response:
        return response['id']
