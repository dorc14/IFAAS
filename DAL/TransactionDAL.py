transactionsList = []

def getTransaction(id):
    for trans in transactionsList:
        if(trans.id == id):
            return trans

def getAllTransactions():
    return transactionsList

def createTransaction(id,status):
    transactionsList.append({id,status})

def changeStatus(id,status):
    for trans in transactionsList:
        if (trans.id == id):
            trans.status = status

