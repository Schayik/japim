# from django.shortcuts import render
from django.http import HttpResponse
from decouple import config
import requests
import json

def index(request):

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    summonerNames = body['data']
    print(summonerNames)

    api_key = config('RIOT_KEY')
    response = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Schayik?api_key=' + api_key)
    data = response.json()
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
