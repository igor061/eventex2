# coding: utf-8

from django import forms
from django.utils.translation import ungettext, ugettext as _
from .models import Subscription

class SubscriptionForm(forms.Form):
    name = forms.CharField(
        label=_('Nome'),
        max_length=100,
    )
    cpf = forms.CharField(
        label=_('CPF'),
        max_length=11,
        min_length=11,
    )
    email = forms.EmailField(
        label=_('Email'),
    )
    phone = forms.CharField(
        label=_('Telefone'),
        required=False,
        max_length=20
    )

    def _unique_check(self, fieldname, error_message):
        param = { fieldname: self.cleaned_data[fieldname]}
        try:
            s = Subscription.objects.get(**param)
        except Subscription.DoesNotExist:
            return param[fieldname]
        raise forms.ValidationError(error_message)

    def clean_cpf(self):
        return self._unique_check('cpf', _(u'CPF já inscrito.'))

    def clean_email(self):
        return self._unique_check('email', _(u'E-mail já inscrito.'))

    def save(self):
        resp = super(SubscriptionForm, self).save()
        resp.name = self.cleaned_data.get('name')
        resp.cpf = self.cleaned_data.get('cpf')
        resp.email = self.cleaned_data.get('email')
        resp.phone = self.cleaned_data.get('phone')


        return resp.save( );