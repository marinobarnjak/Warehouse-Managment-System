from sqlalchemy.orm import Session
from database.connection import engine

def get_db(): 
    with Session(engine) as session:
        yield session 
    

    