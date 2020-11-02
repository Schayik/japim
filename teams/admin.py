from django.contrib import admin
from teams.models import Team, Summoner


class TeamAdmin(admin.ModelAdmin):
    pass


class SummonerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Team, TeamAdmin)
admin.site.register(Summoner, SummonerAdmin)
