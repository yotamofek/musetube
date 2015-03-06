from app.models import Song


class SongMiddleware(object):
    def process_view(self, request, view, args, kwargs):
        if not 'song' in request.session:
            song = Song.objects.create()
            request.session['song'] = song.pk
        else:
            song = Song.objects.get(pk=request.session['song'])
    
        request.song = song