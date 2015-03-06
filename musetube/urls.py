from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.main'),
    url(r'^upload/image/', 'app.views.upload_image'),
    url(r'^upload/audio/', 'app.views.upload_audio'),
    url(r'^submit/$', 'app.views.submit'),
    url(r'^poll_task/$', 'app.views.poll_task'),
    url(r'^google_auth/$', 'app.views.google_auth')
)
