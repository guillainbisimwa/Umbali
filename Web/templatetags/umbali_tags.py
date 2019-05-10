from django import template
from MyEvent.models import MyEventLive

register = template.Library()

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist or Exception as e:
        return None

@register.filter(name='is_owned')
def is_owned(event,user):
    event = get_or_none(MyEventLive,user=user,event=event)
    if event != None:
        return True
    return False
