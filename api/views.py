# from django.shortcuts import render
from django.http import HttpResponse
from decouple import config
import requests
import json

from . import apiFunctions

def index(request):

    inputArray = ['djep0','Chris EDEN']
    print(input)

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

    return HttpResponse(json.dumps(data))
