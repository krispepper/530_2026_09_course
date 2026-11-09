import os 

import mysql.connector
from dotenv import load_dotenv

# env variables
load_dotenv()
USER = os.getenv("USER")
DB = os.getenv("DB")

# Database 
def getDB():
    """Connects to the db or if connection is unsuccessful prints error message."""
    try:
        db = mysql.connector.connect(
            host="localhost",
            user=USER,
            database=DB,
        )

        return db
    except Exception as e:
        return f"Database connections failed: {e}"
