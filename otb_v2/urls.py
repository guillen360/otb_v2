from django.conf.urls import patterns, include, url
#from football.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'otb_v2.views.home', name='home'),
    # url(r'^otb_v2/', include('otb_v2.foo.urls')),
#    (r'^otb/', include('football.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    (r'^scoreboard/$', 'football.views.scoreboard'),
    (r'^team/(?P<team_id>\d+)/$', 'football.views.view_team'),
    (r'^(?P<username>\w+)/$', 'football.views.the_board'),
    (r'^(?P<username>\w+)/(?P<game_id>\d+)/$', 'football.views.create_edit_picks'),
    (r'^$', 'django.contrib.auth.views.login'),
)
