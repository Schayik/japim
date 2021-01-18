from rest_framework import serializers
from teams.models import Team, Summoner, SummonerMatch, Match
from jasper.startPoint import startPoint


class SummonerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summoner
        exclude = ['team']


class TeamSerializer(serializers.ModelSerializer):
    summoners = SummonerSerializer(many=True, read_only=True)
    summoner_names = serializers.ListField(
        required=True,
        write_only=True,
        allow_empty=False,
        max_length=5,
        child=serializers.CharField(),
    )
    matches_total = serializers.SerializerMethodField()
    matches_loaded = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ['id', 'status']

    def create(self, validated_data):
        team = super().create({})

        for summoner_name in validated_data['summoner_names']:
            Summoner.objects.create(team=team, name=summoner_name)

        startPoint(team.id)

        return team

    def intersection(self, obj):
        matchlistArray = [
            summoner.matches.all().values_list('match_id', flat=True)
            for summoner in obj.summoners.all()
        ]
        return set(matchlistArray[0]).intersection(*matchlistArray[1:])

    def get_matches_total(self, obj):
        return len(self.intersection(obj))

    def get_matches_loaded(self, obj):
        intersection = self.intersection(obj)
        matches_loaded = 0
        for match_id in intersection:
            if Match.objects.filter(id=match_id).exists():
                matches_loaded = matches_loaded + 1

        return matches_loaded
