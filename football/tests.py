"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from football.models import Team, Week, Game, UserProfile, Pick

print 'Teams:', Team.objects.all()
print 'Week:', Week.objects.all()
print 'UserProfile:', UserProfile.objects.all()
print 'Pick:', Pick.objects.all()
games = Game.objects.all()
print 'Game:', games
for game in games:
    print '\ngame_date', game.game_date,\
    '\nhome_team', game.home_team,\
    '\naway_team', game.away_team,\
    '\nweek', game.week,\
    '\nspread', game.spread,\
    '\nwinner', game.winner,\
    '\nhome_score', game.home_score,\
    '\naway_score', game.away_score,\
    '\nuserpicks', game.user_picks()
#    '\npick_exists', game.pick_exists(),\
#    '\nhome_team_won', game.home_team_won(),\
#    '\nmark_picks', game.mark_picks(),\
#    '\ncalculate_correct_percentage', game.calculate_correct_percentage(),\
#    '\nuser_picks', game.user_picks()
for game in games:
    print 'game.user_picks()', game.user_picks()
    for pick in game.user_picks():
        print 'pick:', pick.user

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
