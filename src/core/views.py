# coding: utf-8

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic.simple import direct_to_template

from src.core.models import Speaker, Talk


def homepage(request):
    context = RequestContext(request)
    return render_to_response('index.html', context)

def speaker_detail(request, slug):
    speaker = get_object_or_404(Speaker, slug=slug)
    return direct_to_template(request, 'core/speaker_detail.html', {'speaker': speaker})

def talk_detail(request, pk):
    talk = get_object_or_404(Talk, pk=pk)


    return direct_to_template(request, 'core/talk_detail.html', {'talk': talk})


def talks_agenda(request):

    context = {
        'morning_talks': Talk.objects.at_morning(),
        'afternoon_talks': Talk.objects.at_afternoon(),
    }

    return direct_to_template(request, 'core/talks.html', context)

