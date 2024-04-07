from django import template
from django.utils.timesince import timesince as django_timesince
from datetime import datetime

register = template.Library()

@register.filter(name='custom_timesince')
def custom_timesince(time):
    now = datetime.now(time.tzinfo)
    difference = now - time
    
    # If less than a day, show the default `timesince` without the ", x minutes" part
    if difference.days == 0:
        return django_timesince(time).split(",")[0] + " ago"
    else:
        return django_timesince(time) + " ago"