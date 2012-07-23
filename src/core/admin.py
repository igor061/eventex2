# coding: utf-8
from django.contrib import admin
from .models import Contact, Speaker, Talk

class ContactInLine(admin.TabularInline):
    model = Contact
    extra = 1

class SpeakerAdmin(admin.ModelAdmin):
    inlines = [ContactInLine, ]
    prepopulated_fields = { 'slug': ('name', )}

class TalkAdmin(admin.ModelAdmin):
    pass

admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Talk, TalkAdmin)