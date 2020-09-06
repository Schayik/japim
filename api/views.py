# from django.shortcuts import render
from django.http import HttpResponse
from decouple import config
import requests
import json

def index(request):

    api_key = config('RIOT_KEY')
    response = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Schayik?api_key=' + api_key)
    data = response.json()

    return HttpResponse(json.dumps(data))
