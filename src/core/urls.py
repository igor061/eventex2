# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('src.core.views',
    url(r'^palestrantes/(?P<slug>[\w-]+)/$', 'speaker_detail', name='speaker_detail'),
    url(r'^palestras/$', 'talks_agenda', name='talks')
)