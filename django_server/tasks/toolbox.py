import json
import time
from multiprocessing import Process

def checkSameTeams (ids,stats,names):
    participants = list(filter( lambda part: part['player']['summonerName'] in (names), ids))
    partIds = list(map( lambda part: part['participantId'], participants))

    partStats = list(filter( lambda part: part['participantId'] in (partIds), stats))
    partTeams = list(map(lambda x: x['teamId'],partStats))
    teamList = list(set(partTeams))

    if len(teamList) == 1:
        return teamList[0]
    else:
        return False
        
def divByZeroAllowed (n, d): 
    if d == 0:
        return 0
    else:
        return n/d
        
def f(name):
    print('hello', name)
    g = open("myfile3.txt", "x")
    time.sleep(10)
    print('doei', name)
    g.write("Now the file has more content!")
    g.close()
    
def startPoint(request):
    summonerList = request["summoners"].split(",")
    print("t2 ", summonerList)
    print("making process")
    p = Process(target=index, args=(summonerList,))
    time.sleep(1)
    p.start()
    print("started process")
    return 1