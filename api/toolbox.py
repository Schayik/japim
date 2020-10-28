import json

def checkSameTeams (ids,stats,names):
    participants = list(filter( lambda part: part['player']['summonerName'] in (names), ids))
    partIds = list(map( lambda part: part['participantId'], participants))

    partStats = list(filter( lambda part: part['participantId'] in (partIds), stats))
    partTeams = list(map(lambda x: x['teamId'],partStats))
    teamList = list(set(partTeams))
    
    print('teamList',teamList)

    if len(teamList) == 1:
        return teamList[0]
    else:
        return False