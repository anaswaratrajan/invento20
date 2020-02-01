from django.contrib import admin
from .models import Event
# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', '_type', 'fee','short_desc','long_desc', 'prize', 'day')
    list_filter = ('category', '_type', 'fee', 'prize')
