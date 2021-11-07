from DAL import HistoryDAL
from datetime import date

def addIf(param,result):
    addedIf = {
        "date" : date.today(),
        "parameter" : param,
        "result" : result
    }
    HistoryDAL.addIf(addedIf)
def getHistory():
    return HistoryDAL.getAllHistory()
