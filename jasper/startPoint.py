import json
import time
from multiprocessing import Process
from jasper.views import index
from jasper.views import t1

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
    print("t2 ", team_id)
    print("making process")
    print("started process")
    time.sleep(10)
    t1(team_id)
    time.sleep(10)
    index(team_id)
    return 1
