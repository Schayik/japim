import time
from . import tasks
from teams.models import Team
from background_task import background


@background(schedule=1)
def startPoint(team_id):

    try:
        print("starting process")
        team = Team.objects.get(pk=team_id)

        team.status = 'FETCH_IDS'
        team.save()
        print("Updated status to FETCH_IDS")
        tasks.get_riot_ids(team_id)             # Get Riot IDS

        team.status = 'FETCH_MATCH_LISTS'
        team.save()
        print("Updated status to FETCH_MATCH_LISTS")
        tasks.get_matchlists(team_id)           # Get Matchlists

        team.status = 'FETCH_MATCHES'
        team.save()
        print("Updated status to FETCH_MATCHES")
        tasks.get_matches(team_id)              # Get Matches

        team.status = 'COMPLETED'
        team.save()
        print("Updated status to COMPLETED")

    except Exception as exception:
        team.status = 'FAILED'
        team.save()
        print("Updated status to FAILED")
        raise exception
