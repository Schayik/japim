from rest_framework import serializers
from teams.models import Team, Summoner


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
        print(validated_data)
        return super().create({})
