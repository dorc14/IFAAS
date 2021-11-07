import celery

from DAL import IFDAL
from BL import HistoryBL
import requests
import json
from celery_config import make_celery
from app import app

make_celery(app)

def getIf(id):
    wantedIf = IFDAL.getIf(id)
    response = {
        "id": wantedIf["id"],
        "name": wantedIf["name"],
        "properties": wantedIf["properties"],
        "url": {
            "if-execute": wantedIf["url"]["if-execute"]
        }
    }
    jsonStr = json.dumps(response)
    jsonResponse = json.loads(jsonStr)
    return jsonResponse

def getAllIfs():
    allIfs = IFDAL.getAllIfs()
    jsonStr = json.dumps(allIfs)
    jsonResponse = json.loads(jsonStr)
    return jsonResponse

@celery.Task
def createIf(name,properties, url = None):
    tranStatus = 'Failed'
    body = {
            "name": name,
            "properties": properties,
            "url" : url
        }
    jsonStr = json.dumps(body)
    jsonBody = json.loads(jsonStr)

    transid = requests.post("https://ifaas-heroku.herokuapp.com/if",json= jsonBody).json()["transactionId"]
    while(tranStatus != 'SUCCEEDED' ):
        transaction = requests.get("https://ifaas-heroku.herokuapp.com/transactions/" + transid).json()
        tranStatus = transaction["status"]

    id = str(transaction["boxId"])
    executeUrl = "https://127.0.0.1:5000/if/" + name + "/execute"
    IFDAL.createIf(id,name,properties,executeUrl)
    webhookBody = {
        "name":name,
        "url": executeUrl
    }
    strWebhook = json.dumps(webhookBody)
    jsonBodyWe = json.loads(strWebhook)
    requests.post(url,json=jsonBodyWe)
    return transaction

def execIf(name,param):
    id = IFDAL.getIdByName(name)
    jsonStr = json.dumps(param)
    jsonBody = json.loads(jsonStr)

    ifResult = requests.post("https://ifaas-heroku.herokuapp.com/if/" + id + "/execute",json= jsonBody).json()
    HistoryBL.addIf(param,ifResult["result"])
    return ifResult

