from rest_framework import serializers
from teams.models import Team, Summoner

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
