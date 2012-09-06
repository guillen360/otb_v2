from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from football.models import *
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django import forms
from django.forms import widgets, ValidationError
#from datetime import *
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.timezone import make_aware

def scoreboard(request):
    users = User.objects.exclude(username='vip')
    user_profiles = UserProfile.objects.all()
    current_user = request.user
    current_weeks = Week.objects.filter(picks_due_date__gt=timezone.now())
    week_counter = 1
    try:
        current_week = current_weeks[0]
        current_games = Game.objects.filter(week=current_week)
    except IndexError:
        current_week = None
        current_games = None

    previous_weeks = Week.objects.filter(picks_due_date__lt=timezone.now())
    previous_games = []
    for week in previous_weeks:
        games = Game.objects.filter(week=week)
        for game in games:
            previous_games.append(game)

    return render_to_response('scoreboard.html', {'current_user': current_user, 'users': users, 'current_week': current_week,
                                                  'current_games': current_games, 'user_profiles': user_profiles, 'previous_weeks': previous_weeks, 'previous_games': previous_games })

def the_board(request, username):
    user = User.objects.filter(username=username)
    if not user:
        print 'error retrieving user info'

    current_user = User.objects.filter(username=request.user)
    messages = []
    profile = get_object_or_404(UserProfile, user=user)
    correct_percentage = profile.correct_percentage

    current_week_array = Week.objects.filter(picks_due_date__gt=timezone.now())
    try:
        current_week = current_week_array[0]
        current_games_list = Game.objects.filter(week=current_week)
        current_user_picks = {}
        for game in current_games_list:
            if game.pick_exists(user):
                pick = Pick.objects.get(game=game, user=user)
                current_user_picks[game.id] = pick.choice.nickname
            else:
                current_user_picks[game.id] = 'create'
    except IndexError:
        current_week = None
        current_games_list = None
        current_user_picks = None

    previous_weeks = Week.objects.filter(picks_due_date__lt=timezone.now())
    previous_games_list = []
    for week in previous_weeks:
        games = Game.objects.filter(week=week)
        for game in games:
            previous_games_list.append(game)
    previous_user_picks = Pick.objects.filter(user=user)

    context = {
            'user': user[0],
            'current_week': current_week,
            'current_games_list': current_games_list,
            'current_user': current_user[0],
            'current_user_picks': current_user_picks,
            'previous_games_list': previous_games_list,
            'previous_user_picks': previous_user_picks,
            'correct_percentage': correct_percentage,
            'messages': messages,
    }
    return render_to_response('theboard.html', context)

def game_date_compare(x, y):
    if x.game_date > y.game_date:
        return 1
    elif x.game_date == y.game_date:
        return 0
    else:
        return -1

def view_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    current_user = request.user
    home_games = Game.objects.filter(home_team=team)
    away_games = Game.objects.filter(away_team=team)
    team_games = []
    for game in home_games:
        team_games.append(game)
    for game in away_games:
        team_games.append(game)
    team_games.sort(game_date_compare)

    return render_to_response('view_team.html', {'current_user': current_user, 'team': team, 'team_games': team_games, })

class PicksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        choice_choices = kwargs['choice_choices']
        del kwargs['choice_choices']
        super(PicksForm, self).__init__(*args, **kwargs)
        self.fields['choice'].choices = choice_choices

    class Meta:
        model = Pick
        fields = ('choice',)

@login_required
def create_edit_picks(request, username, game_id):
    user = get_object_or_404(User, username=username)
    game = get_object_or_404(Game, id=game_id)
    picks = Pick.objects.filter(game=game, user=user)
    choice_choices = [(game.home_team.id, game.home_team.nickname), (game.away_team.id, game.away_team.nickname)]

    if user != request.user:
#        user.message_set.create(message="You cannot edit %s's picks." %username)
        return HttpResponseRedirect(reverse('football.views.the_board', args=(username,)))

    if timezone.now() > game.week.picks_due_date:
        title = 'View Your Pick!'
        object_description = 'View Your Pick!'
        return render_to_response('view_picks.html', {
            'title': title, 'object_description': object_description, 'game': game, 'pick': pick[0],
            } )

    if request.POST:
        if len(picks) > 0:
            pick = picks[0]
            form = PicksForm(request.POST, instance=pick, choice_choices=choice_choices)
        else:
            form = PicksForm(request.POST, choice_choices=choice_choices)
        if form.is_valid():
            pick = form.save(commit=False)
            pick.user = user
            pick.game = game
            pick.week = game.week

            pick.save()
#            if pick.choice.nickname == 'OU':
#                user.message_set.create(message="OU, huh?  Good luck with that.")
#            else:
#                user.message_set.create(message='OK, you picked %s.  Good luck!' %pick.choice.nickname)
            return HttpResponseRedirect(reverse('football.views.the_board', args=(username,)))
    else:
        if len(picks) > 0:
            pick = picks[0]
            form = PicksForm(instance=pick, choice_choices=choice_choices)
        else:
            form = PicksForm(choice_choices=choice_choices)
        title = 'Make Your Pick!'
        object_description = 'Make Your Pick!'
        return render_to_response('create_edit_picks.html', {
            'title': title, 'object_description': object_description, 'game': game, 'form': form
        }, context_instance=RequestContext(request)
        )