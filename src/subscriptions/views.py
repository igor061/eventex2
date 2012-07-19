# coding: utf-8
# Create your views here.
from django.core.mail import send_mail
from django.conf import settings
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

from .forms import SubscriptionForm
from .models import Subscription

def subscribe(request):
    if request.method == 'POST':
        return subscribeDoPost(request)
    else:
        return openSubscription(request, SubscriptionForm())

def subscribeDoPost(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return openSubscription(request, form)


    subscription = form.save()
    send_mail(subject=u'Cadastro com Sucesso no EventeX',
              message=u'Obrigado pela sua inscrição!',
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[subscription.email],
    )

    return HttpResponseRedirect(reverse('subscriptions:success', args=[subscription.pk]))


def openSubscription(request, form):
    return direct_to_template(request, 'subscriptions/subscription_form.html',
        {'form': form})

def success(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    return direct_to_template(request, 'subscriptions/subscription_detail.html',
                               {'subscription': subscription})

