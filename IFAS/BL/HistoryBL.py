from DAL.HistoryDAL import historyData
from datetime import date

historyAccsess = historyData()

def addIf(param,result):
    historyAccsess.addIf(date.today(), param, result)

def history():
    return historyAccsess.getAllHistory()

