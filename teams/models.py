from django.db import models


class Team(models.Model):
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    FETCH_IDS = "FETCH_IDS"
    FETCH_MATCH_LISTS = "FETCH_MATCH_LISTS"
    FETCH_MATCHES = "FETCH_MATCHES"
    STATUS_CHOICES = [
        (WAITING, 'Waiting'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
        (FETCH_IDS, 'Fetch IDs'),
        (FETCH_MATCH_LISTS, 'Fetch match lists'),
        (FETCH_MATCHES, 'Fetch matches'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=WAITING,
    )

    def __str__(self):
        return str(self.pk)


class Summoner(models.Model):
    name = models.CharField(max_length=200)
    riot_id = models.CharField(max_length=200, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="summoners")

    def __str__(self):
        return self.name


class SummonerMatch(models.Model):
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE, related_name="matches")
    match_id = models.IntegerField()
    
    def __str__(self):
        return str(self.match_id)


class Match(models.Model):
    data = models.JSONField()
