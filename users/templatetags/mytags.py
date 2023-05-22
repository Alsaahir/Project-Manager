from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter(name='is_user_online')
def is_user_online(user):
    if not user.is_authenticated:
        return False

    last_activity = user.profile.last_activity
    offset_naive_datetime = last_activity.replace(tzinfo=None)
    threshold = timedelta(minutes=5)
    return datetime.now() - offset_naive_datetime <= threshold