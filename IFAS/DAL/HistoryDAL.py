from db import db_connection
from sqlalchemy import text

def getAllHistory():
    db = db_connection()
    history = db.execute(text("SELECT * FROM history")).mappings().all()
    return history

def addIf(date,params,result):
    db = db_connection()
    db.execute(text("INSERT INTO ifs VALUES (:date,:params,:result)"),
               {"date": date, "params": params, "result": result})
