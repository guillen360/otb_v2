from django.db import models
from django.contrib.auth.models import User
from decimal import *

getcontext().prec = 2

class Team(models.Model):
    school = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    mascot = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['school']

    def __unicode__(self):
        return self.school

class Week(models.Model):
    start_date = models.DateField()
    picks_due_date = models.DateTimeField()
    season_week = models.IntegerField()

    def __unicode__(self):
        return str(self.start_date)

class Game(models.Model):
    WINNER_CHOICES = (('H', 'Home'), ('A', 'Away'),)
    game_date = models.DateTimeField()
    home_team = models.ForeignKey(Team, related_name='home_games')
    home_team_rank = models.IntegerField(null=True, blank=True)
    away_team = models.ForeignKey(Team, related_name='away_games')
    away_team_rank = models.IntegerField(null=True, blank=True)
    week = models.ForeignKey(Week, related_name='games')
    spread = models.IntegerField(null=True, blank=True)
    winner = models.CharField(max_length=1, choices=WINNER_CHOICES, null=True, blank=True)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "%s vs %s" % (self.home_team.nickname, self.away_team.nickname)

    def pick_exists(self, user):
        pick = Pick.objects.filter(game=self).filter(user=user)
        if pick:
            return True
        else:
            return False

    def home_team_won(self):
        if self.home_score + self.spread > self.away_score:
            return True
        else:
            return False

    def mark_picks(self, request):
        game_picks = Pick.objects.filter(game=self)
        for pick in game_picks:
            if pick.beats_the_spread(request):
                pick.correct = True
                pick.save()
            else:
                pick.correct = False
                pick.save()

    def calculate_correct_percentage(self, request):
        users = User.objects.all()
        for user in users:
            profiles = UserProfile.objects.filter(user=user)
            profile = profiles[0]
            correct_user_picks = Pick.objects.filter(user=user).filter(correct=True)
            total_picks_from_scored_games = Pick.objects.filter(user=user).filter(game__winner__gte='A')
            if len(total_picks_from_scored_games) == 0:
                decimal = 0
            else:
                decimal = float(len(correct_user_picks))/float(len(total_picks_from_scored_games))
            correct_percentage = str(decimal * 100.00)
            profile.correct_percentage = Decimal(correct_percentage)
            profile.save()

    def user_picks(self):
        users = User.objects.exclude(username='vip')
        user_picks = []
        for user in users:
            pick = Pick.objects.filter(game=self, user=user)
            if len(pick) > 0:
                user_picks.append(pick[0])
            else:
                user_picks.append(user)

        return user_picks

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    correct_percentage = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        permissions = (('can_create', 'Can create new weeks, games'), ('can_score', 'Can edit game scores and mark picks correct'),)

class Pick(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    week = models.ForeignKey(Week)
    choice = models.ForeignKey(Team)
    correct = models.NullBooleanField(null=True, blank=True)

    class Meta:
        unique_together = (("user", "game"),)

    def __unicode__(self):
        return "%s picking %s on %s" % (self.user.username, self.choice.school, self.week.start_date)

    def beats_the_spread(self, request):
        if self.game.home_score + self.game.spread > self.game.away_score:
            if self.choice == self.game.home_team:
                return True
            else:
                return False
        else:
            if self.choice == self.game.home_team:
                return False
            else:
                return True

    def get_absolute_url(self):
        return "/%s/%s" % (self.user.username, self.game.id)