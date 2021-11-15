from sqlalchemy import create_engine

def db_connection():
    db = create_engine("sqlite:///ifaas.db")
    connection = db.connect()
    return connection
