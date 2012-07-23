# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import time

# Create your models here.

class Speaker(models.Model):
    name = models.CharField(_('Nome'), max_length=255)
    slug = models.SlugField(_('Slug'), unique=True)
    url = models.URLField(_('Url'))
    description = models.TextField(_(u'Descrição'), blank=True)
    avatar = models.FileField(_('Avatar'), upload_to='palestrantes', blank=True, null=True)

    def __unicode__(self):
        return self.name



##################################
##                CONTACT
#################################

## Managers
class KindContactManager(models.Manager):
    def __init__(self, kind):
        super(KindContactManager, self).__init__()
        self.kind = kind

    def get_query_set(self):
        qs = super(KindContactManager, self).get_query_set()
        qs = qs.filter(kind=self.kind)
        return qs


## Model
class Contact(models.Model):
    KINDS = (
        ('P', _('Telefone')),
        ('E', _('E-mail')),
        ('F', _('Fax')),
    )

    ################
    ## Propiedades
    ########
    speaker = models.ForeignKey('Speaker', verbose_name=_('Palestrante'))
    kind = models.CharField(_('Tipo'), max_length=1, choices=KINDS)
    value = models.CharField(_('Valor'), max_length=255)

    ##############
    ## Meus Managers
    ####
    objects = models.Manager()
    phones = KindContactManager('P')
    emails = KindContactManager('M')
    faxes  = KindContactManager('F')


###############################
##                 Talk
###############################

## Managers
class PeriodManager(models.Manager):
    midday = time(12)

    def at_morning(self):
        qs = self.filter(start_time__lt=self.midday)
        qs = qs.order_by('start_time')
        return qs

    def at_afternoon(self):
        qs = self.filter(start_time__gte=self.midday)
        qs = qs.order_by('start_time')
        return qs

##  Model
class Talk(models.Model):

    ####################
    ## Propriedades
    ######
    title = models.CharField(_(u'Título'), max_length=50, unique=True)
    description = models.TextField(_(u'Descrição'), blank=True)
    start_time = models.TimeField(blank=True)


    objects = PeriodManager()

    def __unicode__(self):
        return self.title

