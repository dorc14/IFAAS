import requests
from DAL import TransactionDAL
import uuid

def createTransaction(status):
    id = uuid.uuid1()
    TransactionDAL.createTransaction(id,status)
def changeStatus(id,status):
    TransactionDAL.changeStatus(id,status)

def getTransaction(id):
    transaction = requests.get("https://ifaas-heroku.herokuapp.com/transactions/" + id).content
    return transaction