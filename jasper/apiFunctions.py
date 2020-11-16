# from django.shortcuts import render
from django.http import HttpResponse
from decouple import config
import requests
import json
import time

def Invoke_API (method,request,extras='',retryTimeOut=0,safetyValue=0,r=''):
    if safetyValue > 50:
        print('safetyValue exceeded, throw! value: ', safetyValue)
        if r != '':
            r.raise_for_status()     ## THROWS ERROR
        else:
            raise ValueError('Recursive safetyValue exceeded by unknown error')     ## THROWS ERROR
    if retryTimeOut > 0:
        print('timed out, timer, safety: ',retryTimeOut,', ', safetyValue)
        time.sleep(retryTimeOut)
        
    baseURL = 'https://euw1.api.riotgames.com/'
    apiKey = config('RIOT_KEY')
    requestURL = baseURL + method + request + '?api_key=' + apiKey
    print("req: ", requestURL)
    response = requests.get(requestURL)
    
    if response.status_code == 200:
        pass
        print('Call succesfull')
    elif response.status_code == 429:  
        retryTimeOutStr = response.headers['retry-after']
        safetyValue+=1
        print('429 error, calling recursive with retry, safety: ',retryTimeOutStr,', ', safetyValue)
        response = Invoke_API(method,request,extras,int(retryTimeOutStr),safetyValue,response)
        return response
    else:
        safetyValue+=26
        retryTimeOutStr = '10'
        print('different error: ', response.status_code, ' safety: ', safetyValue) 
        response = Invoke_API(method,request,extras,int(retryTimeOutStr),safetyValue,response)
        return response
    
    print('end of function returning response, response value = ',response)
    responseData = response.json()
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
