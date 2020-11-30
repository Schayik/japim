from django.test import TestCase
from teams.models import Team, Summoner


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

        print(team.summoners.all())
