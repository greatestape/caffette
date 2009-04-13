# -*- encoding: utf-8 -*-

import datetime

from django import template
from django.template.loader import render_to_string

from ttc_tracker.models import Stop


register = template.Library()


class StopsNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = Stop.objects.all()

        return ""


@register.tag
def get_stops(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        arg = None

    if not arg:
        var_name = 'stops'
    else:
        m = re.search(r"as (\w+)", arg)
        if not m:
            raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
        else:
            var_name = m.groups()

    return StopsNode(var_name)


@register.filter
def rough_wait(dt):
    now = datetime.datetime.now()
    diff = dt - now
    minutes = int(diff.seconds / 60.0)
    seconds = diff.seconds - minutes * 60
    if datetime.timedelta(seconds=-30) < diff < datetime.timedelta(seconds=30):
        template = 'ttc_tracker/includes/arriving.html'
    else:
        template = 'ttc_tracker/includes/wait_time.html'
        return render_to_string(template, {
                'minutes': minutes,
                'seconds': seconds,
                'over_30_seconds': seconds > 30,
                })
rough_wait.is_safe = True