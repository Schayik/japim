# from django.shortcuts import render
from django.http import HttpResponse
from decouple import config
import requests
import json

from . import apiFunctions

class ksScoreObject:
    def __init__(self, summonerName):
        self.summonerName       = summonerName
        self.ksScore            = 0
        self.kills              = 0
        self.killPercentage     = 0
        self.damage             = 0
        self.damagePercentage   = 0
        
    def calculateValues(self):
        pass

def index(request):

    inputArray = ['djep0','Chris EDEN']
    print(inputArray)
    
    matchlistArray = []
    ksScoreData = []
    summonerList = []
    
    for summonerName in inputArray:
        accountId = apiFunctions.Get_AccountID(summonerName)
        summonerKsScoreObject = ksScoreObject(accountId['name'])
        ksScoreData.append(summonerKsScoreObject)
        summonerList.append(accountId['name'])
        matchlist = apiFunctions.Get_Matchlist(accountId['accountId'])
        matchlistArray.append(matchlist)
        
    matchesToLoad = set(matchlistArray[0]).intersection(*matchlistArray)
    
    
    print('matchesToLoad',matchesToLoad)
    print('ksScoreData',ksScoreData[0].__dict__)
    print('summonerList',summonerList)
    #t1 = ksScoreData[0].__dict__
    #print('ksScoreData2',json.dumps(t1))
    #print('ksScoreData',json.dumps(ksScoreData[0].__dict__))
    
    #matchDataArray = []
    totalGames = len(matchesToLoad)
    totalKills = 0
    totalDamage = 0
    
    for matchID in matchesToLoad:
        matchData = apiFunctions.Get_MatchData(matchID)
        #matchDataArray.append(matchData)
        #t1 = list(filter(lambda userData: userData['player']['summonerName'] in summonerList,matchData['participantIdentities']))
        #print('t1',t1)
        correctTeam = True
        teams = []
        teamDmg = []
        teamKills = []
        for i in range(len(matchData['participants'])):
            if matchData['participants'][i]['teamId'] in teams:
                teamIndex = teams.index(matchData['participants'][i]['teamId'])
                teamDmg[teamIndex] += matchData['participants'][i]['stats']['kills']
                teamDmg[teamIndex] += matchData['participants'][i]['stats']['totalDamageDealtToChampions']
            else:
                teams.append(matchData['participants'][i]['teamId'])
                teamDmg.append(matchData['participants'][i]['stats']['kills'])
                teamKills.append(matchData['participants'][i]['stats']['totalDamageDealtToChampions'])
            if matchData['participantIdentities'][i]['player']['summonerName'] in summonerList:
                participantId = matchData['participantIdentities'][i]['participantId']
                statIndex = list(map(lambda x: x['participantId'],matchData['participants'])).index(participantId)
                summonerObjectIndex = summonerList.index(matchData['participantIdentities'][i]['player']['summonerName'])
                ksScoreData[summonerObjectIndex].kills += matchData['participants'][i]['stats']['kills']
                ksScoreData[summonerObjectIndex].damage += matchData['participants'][i]['stats']['totalDamageDealtToChampions']
                
                if correctTeam == True:
                    correctTeam = matchData['participants'][i]['teamId']
                elif correctTeam:
                    if correctTeam == matchData['participants'][i]['teamId']:
                        pass
                    else:
                        correctTeam = False
                else:
                    pass
                    
            
            
        #print('matchDataTest',matchData['participantIdentities'])

    print('ksScoreData2',ksScoreData[0].__dict__)

    dummyData = {
        'games': 10,
        'kills': 23,
        'damage': 24,
        'ksScoreData': [
            {
                'summonerName': 'Djep0', 
                'ksScore': 1, 
                'kills': 12, 
                'killPercentage': 32,
                'damage': 100, 
                'damagePercentage': 24
            },
            {
                'summonerName': 'Snitsky', 
                'ksScore': 1.2, 
                'kills': 34, 
                'killPercentage': 34,
                'damage': 123, 
                'damagePercentage': 51
            }
        ]
    }
    
    #print(dummyData)
    
    return HttpResponse(json.dumps(dummyData))
