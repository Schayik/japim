# from django.shortcuts import render
from django.http import HttpResponse
from decouple import config
import requests
import json

def Invoke_API (method,request,extras=''):
    baseURL = 'https://euw1.api.riotgames.com/'
    apiKey = config('RIOT_KEY')
    requestURL = baseURL + method + request + '?api_key=' + apiKey
    response = requests.get(requestURL)
    responseData = response.json()
    #print('api1',responseData)
    return responseData

def Get_AccountID (summonerName):
    method = 'lol/summoner/v4/summoners/by-name/'
    request = summonerName
    result = Invoke_API(method,request)
    return result

def Get_Matchlist (accountID):
    method = "lol/match/v4/matchlists/by-account/"
    request = accountID
    extras = '&queue=400&queue=420&queue=430&queue=440&queue=700'
    result = Invoke_API(method,request,extras)
    gameIds = map(lambda json_str: json_str['gameId'],result['matches'])    
    return list(gameIds)
    
def Get_MatchData (matchID):
    method = "lol/match/v4/matches/"
    request = str(matchID)
    result = Invoke_API(method,request)
    return result

def test1(sumName,api_key):

    #api_key = config('RIOT_KEY')
    response = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + sumName + '?api_key=' + api_key)
    data = response.json()
    return data
    #return HttpResponse(json.dumps(data))
