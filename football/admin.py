from django.contrib import admin
from football.models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site
from django import forms

class TeamAdmin(admin.ModelAdmin):
    list_display = ('school', 'nickname', 'mascot')

class GameAdmin(admin.ModelAdmin):
    list_display = ('away_team', 'home_team', 'spread', 'game_date', 'week', 'winner', 'score')
    list_filter = ('home_team', 'away_team', 'week')
    date_hierarchy = 'game_date'

    def score(self, obj):
        return ("%s - %s" % (obj.home_score, obj.away_score))

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.winner:
            obj.mark_picks(request)
            obj.calculate_correct_percentage(request)

class PickAdmin(admin.ModelAdmin):
    list_display = ('week', 'game', 'choice', 'user')
    list_filter = ('user', 'week')

class GameInline(admin.TabularInline):
    model = Game
    extra = 6
    max_num = 10
    fields = ('game_date', 'away_team', 'away_team_rank', 'home_team', 'home_team_rank', 'spread', 'winner', 'away_score', 'home_score')

class WeekAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'picks_due_date', 'season_week')
    list_filter = ('season_week',)
    inlines = (GameInline,)
    fieldsets = (('Week Info', {'fields': ('start_date', 'picks_due_date', 'season_week')}),)
    date_hierarchy = 'start_date'

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.games:
            for game in obj.games.all():
                if game.winner:
                    game.mark_picks(request)
                    game.calculate_correct_percentage(request)

class UserProfileInline(admin.TabularInline):
    model = UserProfile
    max_num = 1
    verbose_name = 'Profile'

class UserProfileUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'first_name', 'last_name')
    fieldsets = (
        ('User Info', {
            'fields': ('username', 'password', 'first_name', 'last_name', 'email')
        }),
        )

admin.site.unregister(User)
admin.site.unregister(Site)
admin.site.unregister(Group)
admin.site.register(User, UserProfileUserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Pick, PickAdmin)
admin.site.register(Week, WeekAdmin)