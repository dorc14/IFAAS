from DAL import IFDAL
from BL import HistoryBL
import requests
import json
import validators
from tasks import getTrans

def getIf(id):
    iflist = []
    wantedIf = IFDAL.getIf(id)
    iflist.append(wantedIf)
    return iflist

def getAllIfs():
    allIfs = IFDAL.getAllIfs()
    return makeJsonBody(allIfs)

def createIf(name,properties, url = None):
    body = {
        "name": name,
        "properties":{
            "expression": properties
        },
        "url" : url
    }
    requestBody = makeJsonBody(body)

    transid = requests.post("https://ifaas-heroku.herokuapp.com/if",json= requestBody).json()["transactionId"]
    result = getTrans.delay(transid)
    transaction = result.get()
    if transaction['status'] == 'SUCCEEDED':
        id = str(transaction["boxId"])
        executeUrl = "https://127.0.0.1:5000/if/" + name + "/execute"
        IFDAL.createIf(id,name,properties,executeUrl)
        transaction['executeUrl'] = executeUrl
        webhookBody = {
            "name": name,
            "url": executeUrl
        }
        urlBody = makeJsonBody(webhookBody)

        ''''requests.post(url, json=urlBody)'''''
    else:
        print("There was an error creating the if" + transaction["error"])
        error = {
            "error": transaction["error"]
        }
        errBody = makeJsonBody(error)
        ''''requests.post(url, json=errBody)'''''
    return transaction

def execIf(name,param):
    id = IFDAL.getIdByName(name)
    jsonBody = makeJsonBody(param)

    ifResult = requests.post("https://ifaas-heroku.herokuapp.com/if/" + id + "/execute",json= jsonBody).json()
    HistoryBL.addIf(param,ifResult["result"])
    return ifResult

def makeJsonBody(body):
    jsonStr = json.dumps(body)
    jsonBody = json.loads(jsonStr)
    return jsonBody