import os 

import mysql.connector
from dotenv import load_dotenv

# env variables
load_dotenv()
USER = os.getenv("USER")
DB = os.getenv("DB")

# Connect to Database 
def getDB(): 
    """Check to see if the database connects. If not, then print an error message."""
    try: 
        db = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user=USER,
            database=DB
        )
        return db 
    except Exception as e: 
        return (f"Database connection failed: {e}")

# Create a User (role identified ties the user to their respective table)
def createUser(userID, firstName, lastName, email, role): 
    # SQL: INSERT INTO 'user' (userID, firstName, lastName, email, role) VALUES (%s, %s, %s, %s, %s)
    db = getDB()
    cursor = db.cursor()

    query = """INSERT INTO `user` (userID, firstName, lastName, email, role) VALUES (%s, %s, %s, %s, %s)"""
    values = (userID, firstName, lastName, email, role) 

    cursor.execute(query, values)
    db.commit()

    cursor.close()
    db.close() 

# Add (like an import) 10 Standard Questions (these are on every form).
def add_standardQuestions(eval_ID): 
    db = getDB()
    cursor = db.cursor()

    query = """INSERT INTO formField (fieldID,evalID, title, fieldType, fieldSubject, options) VALUES (%s, %s, %s, %s, %s, %s)"""

    questions = [
        (1, eval_ID, "The instructor presents the subject matter in a clear and understandable way.", "int", "instructor", "1,2,3,4,5,NA"),
        (2, eval_ID, "The instructor uses class time effectively and efficiently.", "int", "instructor", "1,2,3,4,5,NA"),
        (3, eval_ID, "The instructor creates an atmosphere that encourages questions and discussion.", "int", "instructor", "1,2,3,4,5,NA"),
        (4, eval_ID, "The instructor treats students with respect.", "int", "instructor", "1,2,3,4,5,NA"),
        (5, eval_ID, "Exams and assignments are well connected to course objectives.", "int", "course", "1,2,3,4,5,NA"),
        (6, eval_ID, "Assigned materials are relevant to class.", "int", "course", "1,2,3,4,5,NA"),
        (7, eval_ID, "I would recommend this course to other students.", "int", "course", "1,2,3,4,5,NA"),
        (8, eval_ID, "This course has improved my critical thinking skills.", "int", "learning", "1,2,3,4,5,NA"),
        (9, eval_ID, "What did you like most about this course?", "shortText", "misc", None),
        (10, eval_ID, "What suggestions do you have for improving this course?", "shortText", "misc", None)
                ]

    cursor.executemany(query, questions)

    db.commit()
    cursor.close()
    db.close()

# Edit Evaluation Form 
def edit_evaluationQuestion(eval_ID, field_ID, title, fieldType, fieldSubject, options):
    db = getDB() 
    cursor = db.cursor() 

    query = """UPDATE formField SET title = %s, fieldType = %s, fieldSubject=%s, options = %s WHERE evalID = %s AND fieldID = %s"""
    values = (title, fieldType, fieldSubject, options, eval_ID, field_ID)

    cursor.execute(query,values)
    db.commit()

    updatedQuestion = cursor.rowcount

    cursor.close()
    db.close()

    return updatedQuestion

if __name__ == "__main__": 
    db = getDB()
    print(db)
    #print("Database connection was successful.")