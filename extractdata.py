
def extractActionToData(j):
    actiondata = {}
    propertiesdata = {} 

    queryTime = j['time']
    queryType = j['type']
    queryLocX = j['locationX']
    queryLocY = j['locationY']
    queryViewedID = j['viewedId']
    queryPageFrom = j['pageFrom']
    queryPageTo = j['pageTo']

    actiondata['time'] = queryTime
    actiondata['type'] = queryType

    if queryLocX:
        propertiesdata['locationX'] = queryLocX
    if queryLocY:
        propertiesdata['locationY'] = queryLocX
    if queryViewedID:
        propertiesdata['viewedId'] = queryViewedID
    if queryPageFrom:
        propertiesdata['pageFrom'] = queryPageFrom
    if queryPageTo:
        propertiesdata['pageTo'] = queryPageTo

    actiondata['properties'] = propertiesdata
    return actiondata

def extractUserToData(queryUserId, querySessionId):
    userdata = {}
    userdata['userId'] = queryUserId
    userdata['sessionId'] = querySessionId
    userdata['actions'] = []
    return userdata