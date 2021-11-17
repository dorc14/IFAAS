from db import db_connection
from sqlalchemy import text

class ifData:
    def __init__(self):
        self.db = db_connection()

    def getIf(self, id: str) -> list:
        wantedIf = self.db.execute(text("SELECT * FROM ifs WHERE id = :id"),{"id": str(id)}).mappings().all()
        return wantedIf

    def getAllIfs(self) -> list:
        ifs = self.db.execute(text("SELECT * FROM ifs")).mappings().all()
        return ifs

    def createIf(self, id: str, name: str, properties: str, executeUrl: str):
        self.db.execute(text("INSERT INTO ifs VALUES (:id,:name,:properties,:executeUrl)"),
               {"id": id, "name": name, "properties": properties, "executeUrl": executeUrl})

    def getIdByName(self, name: str) -> list:
        Id = self.db.execute(text("select id from ifs where name = :name"),{"name": str(name)}).mappings().all()[0]
        return Id["id"]

    def checkIfExist(self, name: str) -> bool:
        If = self.db.execute(text("select * from ifs where name = :name"),{"name": str(name)}).mappings().all()
        return bool(If)