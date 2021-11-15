from DAL import IFDAL
from BL import HistoryBL
import requests
import json
import validators
from tasks import getTrans
import re


def getIf(id):
    wantedIf = IFDAL.getIf(id)
    return wantedIf

def getAllIfs():
    allIfs = IFDAL.getAllIfs()
    return allIfs

def createIf(name,properties, url = None):
    body = {
        "name": name,
        "properties":{
            "expression": properties
        },
        "url" : url
    }
    requestBody = makeJsonBody(body)
    match = re.search('^[a-z]*[-]+[a-z]+$',name)

    if not IFDAL.checkIfExist(name) and match:
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

        else:
            print("There was an error creating the if" + transaction["error"])
            webhookBody = {
                "error": transaction["error"]
            }
            urlBody = makeJsonBody(webhookBody)
        if(validators.url(url)):
            requests.post(url, json=urlBody)
        else:
            print("Wrong Url pls Change")
    else:
        transaction = {
            "error": "There was an error Creating the if, check the name"
        }

    return transaction

def execIf(name,param):
    id = IFDAL.getIdByName(name)["id"]
    jsonBody = makeJsonBody(param)

    ifResult = requests.post("https://ifaas-heroku.herokuapp.com/if/" + id + "/execute",json= jsonBody).json()
    HistoryBL.addIf(param,ifResult["result"])
    return ifResult

def makeJsonBody(body):
    jsonStr = json.dumps(body)
    jsonBody = json.loads(jsonStr)
    return jsonBody