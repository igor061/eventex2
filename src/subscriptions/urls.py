#  coding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('src.subscriptions.views',
    url(r'^$', 'subscribe', name='subscribe'),
    url(r'^(\d+)/$', 'success', name='success'),
)