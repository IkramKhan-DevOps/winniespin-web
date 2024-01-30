from django.contrib import admin

from .models import (
    Event, Participant, Result
)


class ParticipantInline(admin.TabularInline):
    model = Participant


class ResultInline(admin.StackedInline):
    model = Result
    can_delete = False


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'status', 'spun_on', 'created_on', 'updated_on')
    list_filter = ('event_type', 'status')
    search_fields = ['name', 'description']
    inlines = [
        ParticipantInline, ResultInline
    ]


class ResultAdmin(admin.ModelAdmin):
    list_display = ('participant', 'event')
    search_fields = ['participant__token_number']


admin.site.register(Event, EventAdmin)
admin.site.register(Result, ResultAdmin)