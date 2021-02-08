from django.test import TestCase
from teams.models import Team, Summoner, SummonerMatch


class TeamsTestCase(TestCase):

    def test_models(self):
        team = Team.objects.create()

        # adding summoners
        for name in ["djep0", "schayik", "dirco"]:
            summoner = Summoner(team=team, name=name)
            summoner.save()
            team.summoners.add(summoner)
        team.save()

        # update summoner information
        for (index, summoner) in enumerate(team.summoners.all()):
            summoner.name = summoner.name.capitalize()
            summoner.riot_id = index
            summoner.save()

        # create summoner matches
        for (i, summoner) in enumerate(team.summoners.all()):
            for j in range(1, (i + 1) * 10, i + 1):
                summoner_match = SummonerMatch(summoner=summoner, match_id=j)
                summoner_match.save()

        # obtain overlapping matches
        matchlistArray = [
            summoner.matches.all().values_list('match_id', flat=True)
            for summoner in team.summoners.all()
        ]
        matchesToLoad = set(matchlistArray[0]).intersection(*matchlistArray[1:])
        print(matchesToLoad)
