from celery import Celery
import requests

celery = Celery('tasks',broker='redis://localhost:6379/0',backend='redis://localhost:6379/0')

@celery.task(name="check_status.task")
def getTrans(transId):
    transStatus = 'PENDING'
    while(transStatus == 'PENDING'):
        transaction = requests.get("https://ifaas-heroku.herokuapp.com/transactions/" + transId).json()
        transStatus = transaction["status"]
    return transaction