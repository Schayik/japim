from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from teams.models import Team
from teams.serializers import TeamSerializer
from jasper.startPoint import startPoint
import time

@api_view(['GET', 'POST'])
def team_list(request):
    """
    List all code teams, or create a new team.
    """
    if request.method == 'GET':
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #t1(serializer.data["id"])
            print("t1.1 ",serializer.data)
            summonerList = request.data["summoners"].split(",")
            print("t1.2 ", "hoi")
            print("t1.3 ", summonerList)
            t1 = startPoint(serializer.data["id"])
            print("t3 ", t1)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def team_detail(request, pk):
    """
    Retrieve, update or delete a code team.
    """
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
