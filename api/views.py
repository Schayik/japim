# from django.shortcuts import render
from django.http import HttpResponse
from decouple import config
import requests
import json

from . import apiFunctions

def index(request):

    inputArray = ['djep0','Chris EDEN']
    print(inputArray)

    api_key = config('RIOT_KEY')
    response = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Schayik?api_key=' + api_key)
    data = response.json()
    
    matchlistArray = []
    
    for summonerName in inputArray:
        accountId = apiFunctions.Get_AccountID(summonerName)
        matchlist = apiFunctions.Get_Matchlist(accountId['accountId'])
        matchlistArray.append(matchlist)
        
    matchesToLoad = set(matchlistArray[0]).intersection(*matchlistArray)
    
    print('matchesToLoad',matchesToLoad)
    
    matchDataArray = []
    
    for matchID in matchesToLoad:
        matchData = apiFunctions.Get_MatchData(matchID)
        matchDataArray.append(matchData)

    print(matchDataArray[0])    
    print(data)


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

    return HttpResponse(json.dumps(dummyData))
