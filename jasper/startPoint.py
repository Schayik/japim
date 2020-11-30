import json
import time
from multiprocessing import Process
from jasper import tasks

from teams.models import Team, Summoner

from background_task import background
#from django.contrib.auth.models import User

#@background(schedule=60)
#def notify_user(user_id):
#    # lookup user by id and send them a message
#    user = User.objects.get(pk=user_id)
#    user.email_user('Here is a notification', 'You have been notified')

@background(schedule=1)
def startPoint(team_id):

    print("defined process")
    time.sleep(10)
    
    print("starting process")
    team = Team.objects.get(pk=team_id)

    team.status = 'FETCH_IDS'
    team.save()
    print("Updated status to FETCH_IDS")
    
    time.sleep(5)
    tasks.get_riot_ids(team_id)             ## Get Riot IDS
    time.sleep(5)

    team.status = 'FETCH_MATCH_LISTS'
    team.save()
    print("Updated status to FETCH_MATCH_LISTS")
    
    time.sleep(5)
    tasks.get_matchlists(team_id)           ## Get Matchlists
    time.sleep(5)
    
    team.status = 'FETCH_MATCHES'
    team.save()
    print("Updated status to FETCH_MATCHES")
    
    ## GET MATCHES HERE

    return
