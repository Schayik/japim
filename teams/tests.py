from django.test import TestCase
from teams.models import Team, Summoner, SummonerMatch


class TeamsTestCase(TestCase):

    def test_models(self):
        team = Team.objects.create()

        # adding summoners
        for name in ["djep0", "schayik"]:
            summoner = Summoner(team=team, name=name)
            summoner.save()
            team.summoners.add(summoner)
        team.save()

        # update summoner information
        for (index, summoner) in enumerate(team.summoners.all()):
            summoner.name = summoner.name.capitalize()
            summoner.riot_id = index
            summoner.save()

        # create summoner matcher
        for (i, summoner) in enumerate(team.summoners.all()):
            for j in range(1, (i + 1) * 10, i + 1):
                summoner_match = SummonerMatch(summoner=summoner, match_id=j)
                summoner_match.save()

        # obtain overlapping matches
        # TODO: mooier maken
        first_summoner = team.summoners.all().first()
        intersection = [match.match_id for match in first_summoner.matches.all()]

        for (index, summoner) in enumerate(team.summoners.all()):
            if index == 0:
                pass

            match_ids = [match.match_id for match in summoner.matches.all()]
            intersection = list(set(intersection) & set(match_ids))

        print(intersection)
