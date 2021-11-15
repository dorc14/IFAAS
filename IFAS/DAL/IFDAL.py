from db import db_connection
from sqlalchemy import text

def getIf(id):
    db = db_connection()
    wantedIf = db.execute(text("SELECT * FROM ifs WHERE id = :id"),{"id": str(id)}).mappings().all()
    return wantedIf

def getAllIfs():
    db = db_connection()
    ifs = db.execute(text("SELECT * FROM ifs")).mappings().all()
    return ifs

def createIf(id,name,properties,executeUrl):
    db = db_connection()
    db.execute(text("INSERT INTO ifs VALUES (:id,:name,:properties,:executeUrl)"),
               {"id": id, "name": name, "properties": properties, "executeUrl": executeUrl})

def getIdByName(name):
    db = db_connection()
    ifId = db.execute(text("select id from ifs where name = :name"),{"name": str(name)}).mappings().all()
    return ifId[0]

def checkIfExist(name):
    db = db_connection()
    wantedIf = db.execute(text("select * from ifs where name = :name"),{"name": str(name)}).mappings().all()
    return bool(wantedIf)