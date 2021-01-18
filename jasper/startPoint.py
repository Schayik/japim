import time
from jasper import tasks
from teams.models import Team
from background_task import background


@background(schedule=1)
def startPoint(team_id):

    try:
        print("defined process")
        time.sleep(10)

        print("starting process")
        team = Team.objects.get(pk=team_id)

        team.status = 'FETCH_IDS'
        team.save()
        print("Updated status to FETCH_IDS")

        time.sleep(5)
        tasks.get_riot_ids(team_id)             # Get Riot IDS
        time.sleep(5)

        team.status = 'FETCH_MATCH_LISTS'
        team.save()
        print("Updated status to FETCH_MATCH_LISTS")

        time.sleep(5)
        tasks.get_matchlists(team_id)           # Get Matchlists
        time.sleep(5)

        team.status = 'FETCH_MATCHES'
        team.save()
        print("Updated status to FETCH_MATCHES")

        time.sleep(5)
        tasks.get_matches(team_id)              # Get Matches
        time.sleep(5)

        team.status = 'COMPLETED'
        team.save()
        print("Updated status to COMPLETED")

    except Exception as exception:
        team.status = 'FAILED'
        team.save()
        print("Updated status to FAILED")
        raise exception
