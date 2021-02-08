# from django.shortcuts import render
from django.http import HttpResponse
from decouple import config
import requests
import json
import time

from teams.models import Team, Summoner, SummonerMatch, Match

from riot_api import apiFunctions
from . import toolbox

#class ksScoreObject:
#    def __init__(self, summonerName):
#        self.summonerName       = summonerName
#        self.ksScore            = 0.0
#        self.kills              = 0
#        self.killPercentage     = 0.0
#        self.damage             = 0
#        self.damagePercentage   = 0.0
#        
#    def calculateValues(self,totalKills,TotalDamage):
#        self.killPercentage = toolbox.divByZeroAllowed(self.kills, totalKills)
#        self.damagePercentage = toolbox.divByZeroAllowed(self.damage, TotalDamage)
#        self.ksScore = toolbox.divByZeroAllowed(self.killPercentage, self.damagePercentage)
#        
#    def ksScoreOutput(self):
#        returnObj = {
#            'summonerName'     : self.summonerName                              ,
#            'ksScore'          : '{:.2f}'.format(self.ksScore)                  ,
#            'kills'            : '{:,}'.format(self.kills)                      ,
#            'killPercentage'   : '{:.2f}%'.format(self.killPercentage*100)      ,
#            'damage'           : '{:,}'.format(self.damage)                     ,
#            'damagePercentage' : '{:.2f}%'.format(self.damagePercentage*100)    ,
#        }
#        return returnObj

def get_riot_ids(team_id):
    team = Team.objects.get(pk=team_id)
    for summoner in team.summoners.all():
        summonerInfo = apiFunctions.Get_AccountID(summoner.name)
        summoner.name = summonerInfo['name']
        summoner.riot_id = summonerInfo['accountId']
        summoner.save()
    return

def get_matchlists(team_id):
    team = Team.objects.get(pk=team_id)
    for summoner in team.summoners.all():
        summoner_matchlist = apiFunctions.Get_Matchlist(summoner.riot_id)
        for match_id in summoner_matchlist:
            SummonerMatch.objects.create(summoner=summoner, match_id=match_id)
    return
    
def get_matches(team_id):
    team = Team.objects.get(pk=team_id)
    matchlistArray = [
            summoner.matches.all().values_list('match_id', flat=True)
            for summoner in team.summoners.all()
        ]
    matchesToLoad = set(matchlistArray[0]).intersection(*matchlistArray) 
    for match_id in matchesToLoad:
        if not Match.objects.filter(pk=match_id).exists():
            matchData = apiFunctions.Get_MatchData(match_id)
            Match.objects.create(id=match_id,data=matchData)
    return