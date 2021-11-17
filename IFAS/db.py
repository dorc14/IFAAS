from sqlalchemy import create_engine

def db_connection():
    db = create_engine("sqlite:///ifaas.db",connect_args={"check_same_thread": False})
    connection = db.connect()
    return connection
