from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.auth.models import User

def format_pick(pick, current_user):
    value = ''
    if type(pick) == User:
        if pick == current_user:
            value = '<a href="/otb/' + pick.username + '/' + str(game.id) + '">create</a>'
        else:
            value = 'none'
    else:
        if pick.user == current_user:
            value = '<a href="/otb/' + pick.user.username + '/' + str(game.id) + '">' + pick.choice.nickname + '</a>'
        else:
            value = pick.choice.nickname
    return value

register = template.Library()
register.filter('format_pick', format_pick)