from DAL import HistoryDAL
from datetime import date


def addIf(param,result):
    HistoryDAL.addIf(date.today(),param,result)

def getHistory():
    return HistoryDAL.getAllHistory()
