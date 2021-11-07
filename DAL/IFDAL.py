import json

ifDict = {}
def getIf(id):
    for key,value in ifDict.items():
        if(key == id):
            return value
def getAllIfs():
    values = list(ifDict.values())
    return values

def createIf(id,name,properties,executeUrl):
    body = {
        "id" : id,
        "name": name,
        "properties": properties,
        "url" : {
            "if-execute": executeUrl
        }
    }
    jsonStr = json.dumps(body)
    insertIf = json.loads(jsonStr)
    ifDict[id] = insertIf

def getNameById(id):
    return ifDict.get(id)["name"]

def getIdByName(name):
    for key,value in ifDict.items():
        if (value["name"] == name):
            return key