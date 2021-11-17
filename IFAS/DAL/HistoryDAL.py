from db import db_connection
from sqlalchemy import text

class historyData:
    def __init__(self):
        self.db = db_connection()

    def getAllHistory(self) -> list:
        ifStats = self.db.execute(text("SELECT * FROM history")).mappings().all()
        return ifStats

    def addIf(self, date, params: str, result: str):
        self.db.execute(text("INSERT INTO history VALUES (:date,:params,:result)"),
               {"date": date, "params": str(params), "result": result})
