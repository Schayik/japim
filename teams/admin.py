from django.contrib import admin
from teams.models import Team, Summoner, Match


class TeamAdmin(admin.ModelAdmin):
    pass


class SummonerAdmin(admin.ModelAdmin):
    pass


class MatchAdmin(admin.ModelAdmin):
    pass


admin.site.register(Team, TeamAdmin)
admin.site.register(Summoner, SummonerAdmin)
admin.site.register(Match, MatchAdmin)
