from DAL.IFDAL import ifData
from BL import HistoryBL
import requests
import json
import validators
from tasks import getTrans
import re
from Constants import transactionStatus, ifAssUrl

ifAccess = ifData()

def getIf(id: str) -> list:
    If = ifAccess.getIf(id)
    return If

def getAllIfs() -> list:
    allIfs = ifAccess.getAllIfs()
    return allIfs

def createIf(name: str,properties: str, url: str = None):
    body = {
        "name": name,
        "properties":{
            "expression": properties
        },
        "url" : url
    }
    requestBody = makeJsonBody(body)

    if checkIfValidation(name):
        transactionId = requests.post(ifAssUrl, json= requestBody).json()["transactionId"]
        result = getTrans.delay(transactionId)
        transaction = result.get()
        if transaction['status'] == transactionStatus['SUCCEEDED']:
            id = str(transaction["boxId"])
            executeUrl = "http://127.0.0.1:5000/if/" + name + "/execute"
            ifAccess.createIf(id, name, properties, executeUrl)
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

        checkUrlValidation(url,urlBody)
    else:
        transaction = {
            "error": "There was an error Creating the if, check the name"
        }

    return transaction

def execIf(name: str,param: str) -> dict:
    id = ifAccess.getIdByName(name)
    body = makeJsonBody(param)

    ifResult = requests.post(ifAssUrl + "/" + id + "/execute", json= body).json()
    HistoryBL.addIf(param, ifResult["result"])
    return ifResult

def makeJsonBody(body: dict) -> dict:
    convertJsonToString = json.dumps(body)
    body = json.loads(convertJsonToString)
    return body

def checkIfValidation(name: str) -> bool:
    isIfValid = re.search('^[a-z]*[-]+[a-z]+$', name)
    return not ifAccess.checkIfExist(name) and isIfValid

def checkUrlValidation(url: str, body: dict):
    if validators.url(url):
        requests.post(url, json=body)
    else:
        print("Wrong Url pls Change")




