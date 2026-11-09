import os 

import mysql.connector
from dotenv import load_dotenv

# env variables
load_dotenv()
USER = os.getenv("USER")

# Database 
"""TODO: add db models."""

def getDB():
    """Connects to the db or if connection is unsuccessful prints error message."""
    try:
        db = mysql.connector.connect(
            host="localhost",
            user=USER,
            database="faithmock",
        )

        return db
    except Exception as e:
        return f"Database connections failed: {e}"

def getUAT():
    """Connects to the UAT DB or if connection is unsuccessful prints error message."""
    try:
        db = mysql.connector.connect(
            host="localhost",
            user=USER,
            database="fall2026_530_course",
        )

        return db
    except Exception as e:
        return f"Database connections failed: {e}"
