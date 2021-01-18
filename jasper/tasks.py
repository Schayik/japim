# from django.shortcuts import render
from django.http import HttpResponse
from decouple import config
import requests
import json
import time

from teams.models import Team, Summoner, SummonerMatch, Match
from jasper.toolbox import f


from . import apiFunctions
from . import toolbox

class ksScoreObject:
    def __init__(self, summonerName):
        self.summonerName       = summonerName
        self.ksScore            = 0.0
        self.kills              = 0
        self.killPercentage     = 0.0
        self.damage             = 0
        self.damagePercentage   = 0.0
        
    def calculateValues(self,totalKills,TotalDamage):
        self.killPercentage = toolbox.divByZeroAllowed(self.kills, totalKills)
        self.damagePercentage = toolbox.divByZeroAllowed(self.damage, TotalDamage)
        self.ksScore = toolbox.divByZeroAllowed(self.killPercentage, self.damagePercentage)
        
    def ksScoreOutput(self):
        returnObj = {
            'summonerName'     : self.summonerName                              ,
            'ksScore'          : '{:.2f}'.format(self.ksScore)                  ,
            'kills'            : '{:,}'.format(self.kills)                      ,
            'killPercentage'   : '{:.2f}%'.format(self.killPercentage*100)      ,
            'damage'           : '{:,}'.format(self.damage)                     ,
            'damagePercentage' : '{:.2f}%'.format(self.damagePercentage*100)    ,
        }
        return returnObj

#def t1(x):
#    print("t1",x)
#    cheese_blog = Team.objects.get(pk=x)
#    print("t3",cheese_blog)
#    cheese_blog.status = "FETCH_IDS"
#    inputArray = ['djep0','Schayik']
#    for summonerName in inputArray:
#        Summoner.objects.create(team=cheese_blog,name=summonerName)
#    cheese_blog.save()
#    print("t4",cheese_blog.summoner_count())
    
#def startPoint(request):
#    summonerList = request["summoners"].split(",")
#    print("t2 ", summonerList)
#
#    return 1

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
        print("matchlist of summoner: ", summoner.name)
        print(summoner_matchlist)
        for match_id in summoner_matchlist:
            SummonerMatch.objects.create(summoner=summoner, match_id=match_id)
    return
    
def get_matches(team_id):
    team = Team.objects.get(pk=team_id)
    matchlistArray = [
            summoner.matches.all().values_list('match_id', flat=True)
            for summoner in team.summoners.all()
        ]
    matchesToLoad = set(matchlistArray[0]).intersection(*matchlistArray[1:]) 
    print("matches to load: ",matchesToLoad)
    for match_id in matchesToLoad:
        matchData = apiFunctions.Get_MatchData(match_id)
        Match.objects.create(id=match_id,data=matchData)
    return


def index(request):
    print('t4 ',request)
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        inputArray = body['data']
        print('summoners!',inputArray)
        
    except:
        inputArray = ['djep0','snitsky'] #Chris EDEN
        pass
    
    print(inputArray)
    #f('bob')
    
    
    #api_key = config('RIOT_KEY')
    #response = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Schayik?api_key=' + api_key)
    #data = response.json()
    
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
    totalGames = 0
    totalKills = 0
    totalDamage = 0
    
    for matchID in matchesToLoad:
        start = time.process_time()
        matchData = apiFunctions.Get_MatchData(matchID)
        # print ('find API call time: ', (time.process_time() - start) *1000)
        commonTeam = toolbox.checkSameTeams(matchData['participantIdentities'],matchData['participants'],summonerList)
        if commonTeam:
            pass
        else:
            continue
            
        teamDmg = 0
        teamKills = 0
        statIdsArray = list(map(lambda part: part['participantId'],matchData['participants']))
        
        for i in range(len(matchData['participants'])):
            if matchData['participants'][i]['teamId'] == commonTeam:
                teamKills += matchData['participants'][i]['stats']['kills']
                teamDmg += matchData['participants'][i]['stats']['totalDamageDealtToChampions']
            else:
                continue
                
            if matchData['participantIdentities'][i]['player']['summonerName'] in summonerList:
                participantId = matchData['participantIdentities'][i]['participantId']
                statIndex = statIdsArray.index(participantId)
                
                summonerObjectIndex = summonerList.index(matchData['participantIdentities'][i]['player']['summonerName'])
                ksScoreData[summonerObjectIndex].kills += matchData['participants'][i]['stats']['kills']
                ksScoreData[summonerObjectIndex].damage += matchData['participants'][i]['stats']['totalDamageDealtToChampions']
        
        totalGames += 1
        totalKills += teamKills
        totalDamage += teamDmg

    print('totalGames',totalGames)
    print('totalKills',totalKills)
    print('totalDamage',totalDamage)
    print('ksScoreData2',ksScoreData[0].__dict__)
    
    ksScoreDataArray = []
    
    for summonerKsObject in ksScoreData:
        summonerKsObject.calculateValues(totalKills,totalDamage)
        ksScoreDataArray.append(summonerKsObject.ksScoreOutput())
        print('testje!',summonerKsObject.ksScoreOutput())
        
    print('ksScoreData3',ksScoreData[0].__dict__)
    
    print('ksScoreData4',ksScoreDataArray[0])
    
    print('ksScoreData5',ksScoreDataArray)
    
    realData = {
        'games': '{:,}'.format(totalGames),
        'kills': '{:,}'.format(totalKills),
        'damage': '{:,}'.format(totalDamage),
        'ksScoreData': ksScoreDataArray
    }

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
    
    return HttpResponse(json.dumps(realData))
