from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

register = template.Library()

def format_pick(pick, current_user):
    value = ''
    if type(pick) == User:
        if pick == current_user:
            value = '<a href="/' + pick.username + '/' + '">create</a>'
        else:
            value = 'none'
    else:
        if pick.user == current_user:
#        if pick == current_user:
            value = '<a href="/' + pick.user.username + '/' + str(pick.game.id) + '">' + pick.choice.nickname + '</a>'
        else:
            value = pick.choice.nickname

    value = mark_safe(value)
    return value

def disp_spread(game):
    value = ''
    if game.spread > 0:
        value = '%s by %s' % (game.away_team.nickname, str(game.spread))
    elif game.spread < 0:
        value = '%s by %s' % (game.home_team.nickname, str((game.spread * (-1))))
    else:
        value = 'even'
    return value

register.filter('format_pick', format_pick)
register.filter('disp_spread', disp_spread)

if __name__ == "__main__":
    print User