"""
DATABASE RELATED FUNCTIONS.
"""

import os 

import mysql.connector
from dotenv import load_dotenv

from constants import ROLE

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

# USER FUNCTIONS
def getUserRole(userID: str) -> str:
    """ 
    Given a user ID returns the role (instructor, student, department chair or school admin).

    attrs: 
        userID (str): ID of user
    return: 
        role (str): returns one of these ('stu', 'ins', 'sca', 'dc')
            stu = student
            ins = instructor
            sca = school administrator
            dc = department chair
    """
    # open database connection
    userDB = getDB()
    # cursor fetch will return as dict
    usercursor = userDB.cursor(dictionary=True)

    # query for db
    query = "SELECT role FROM user WHERE userID = %s"
    # run query using instructorID
    usercursor.execute(query, (userID,))
    # get results as dict
    DBresult_dict = usercursor.fetchone()

    # check user was found
    if DBresult_dict is not None:
        # get list of section IDs
        role = DBresult_dict["role"]

        # close DB and cursor
        usercursor.close() 
        userDB.close()

        # return role
        return role
    else:
        # close DB and cursor
        usercursor.close() 
        userDB.close()

        # return error message
        return f"No role found for userID '{userID}'."

def getRoleID(userID: str) -> str:
    """ 
    Given a user ID returns the role specific ID.

    attrs: 
        userID (str): ID of user
    return: 
        roleID (str): ID related to user's specific role (instructorID, adminID, studentID)
    """
    # get user role
    role = getUserRole(userID)

    # set table and id name for query 
    # or return error message if not one of the set four
    if role == ROLE.student.value:
        table = 'student'
        id = 'studentID'
    elif role == ROLE.instructor.value:
        table = 'instructor'
        id = 'instructorID'
    elif role == ROLE.schoolAdmin.value:
        table = 'schoolAdmin'
        id = 'adminID'
    elif role == ROLE.deptChair.value:
        table = 'instructor'
        id = 'instructorID'
    else: 
        # will return if no role is found
        return f"No specialized role ID for userID '{userID}'."
    
    # open database connection
    userDB = getDB()
    # cursor fetch will return as dict
    usercursor = userDB.cursor(dictionary=True)

    # query for db
    query = f"SELECT {id} FROM {table} WHERE userID = %s"
    # run query using userID
    usercursor.execute(query, (userID,))
    # get results as dict
    DBresult_dict = usercursor.fetchone()
    print(DBresult_dict)
    if DBresult_dict is not None:
        # get instructorID
        roleID = DBresult_dict[id]
    
        # close DB and cursor
        usercursor.close() 
        userDB.close()

        # return role specific ID
        return roleID
    else:
        # close DB and cursor
        usercursor.close() 
        userDB.close()

        # return error message
        return f"{userID} NOT FOUND in {table} table."

def getDept(userID: str) -> int:
    """
    Function returns a dict with evaluation responses associated with a given department chair.
        
    attrs: 
        userID (str): id of instructor (or department chair)
    return: 
        dept (int): dept id for a given instructor.
    """
    # open database connection
    userDB = getDB()
    # cursor fetch will return as dict
    usercursor = userDB.cursor(dictionary=True)

    # query for db
    query = "SELECT deptID FROM instructor WHERE userID = %s"
    # run query using instructorID
    usercursor.execute(query, (userID,))
    # get results as dict
    DBresult_dict = usercursor.fetchone()

    # check user was found
    if DBresult_dict is not None:
        # get list of section IDs
        dept = DBresult_dict["deptID"]

        # close DB and cursor
        usercursor.close() 
        userDB.close()

        # return role
        return dept
    else:
        # close DB and cursor
        usercursor.close() 
        userDB.close()

        # return error message
        return f"No dept found for userID '{userID}'."


# EVALUATION FUNCTIONS
def getEvalListInstructor(instructorID: str) -> list[dict]:
    """ 
    Function returns a dict with evaluation responses associated with a given instructor.
    
    attrs: 
        instructorID (str): id of instructor
    return: 
        evalResponses (dict): a dict of evaluation responses associated with a given instructor

    """
    # open database connection
    evalDB = getDB()
    # cursor fetch will return as dictionary
    evalcursor = evalDB.cursor(dictionary=True)

    # query for getting evalIDs
    queryEvalIDs = (
        "SELECT evalID "
        "FROM sections AS s JOIN evaluation AS e ON "
        "s.courseID = e.courseID "
        "AND s.secID = e.secID " 
        "AND s.term = e.term "
        "WHERE instructorID = %s"
        )
    # run query using instructorID
    evalcursor.execute(queryEvalIDs, (instructorID,))
    # get results from query as list 
    evalIDs_list = [eval['evalID'] for eval in evalcursor.fetchall()]

    # convert evalIDs list to string
    evalIDs = ', '.join(evalIDs_list)
    # query for getting evaluation responses
    queryResponses = (
        "SELECT * "
        "FROM evalResponse "
        "WHERE evalID IN (%s) "
        "ORDER BY evalID"
    )
    # run query using evalIDs
    evalcursor.execute(queryResponses, (evalIDs,))
    # get results from query
    evalResponses = evalcursor.fetchall()

    # close DB and cursor
    evalcursor.close() 
    evalDB.close()

    if evalResponses:
        return evalResponses
    else:
        return "No evaluation responses found."

def getEvalListStudent(studentID: str) -> list[dict]:
    """ 
    Function returns a dict with eval responses associated with a given student.
    
    attrs: 
        studentID (str): id of student
    return: 
        evalResponses (dict): a dict of evaluation responses associated with a given student
    """
    # open database connection
    evalDB = getDB()
    # cursor fetch will return as dict
    evalcursor = evalDB.cursor(dictionary=True)

    # query for db
    query = (
        "SELECT * "
        "FROM evalResponse "
        "WHERE studentID = %s "
        "ORDER BY evalID, studentID, fieldID"
    )
    # run query using section IDs
    evalcursor.execute(query, (studentID,))
    # get results as dict
    evalResponses = evalcursor.fetchall()

    # close DB and cursor
    evalcursor.close() 
    evalDB.close()
    if evalResponses:
        return evalResponses
    else:
        return "No evaluation responses found."

def getEvalListDeptChair(deptChairID: str) -> list[dict]:
    """ 
    Function returns a dict with evaluation responses associated with a given department chair.
    
    attrs: 
        deptChairID (str): id of department chair
    return: 
        evalResponses (dict): a dict of evaluation responses associated with a given dept chair.
    """

    # get dept for deptChair
    dept = getDept(deptChairID)

    # open database connection
    evalDB = getDB()
    # cursor fetch will return as dictionary
    evalcursor = evalDB.cursor(dictionary=True)

    # query for getting evalIDs
    queryEvalIDs = (
            "WITH instructorEval (instructorID, evalID) AS ("
            "SELECT s.instructorID, e.evalID "
            "FROM sections AS s "
            "JOIN evaluation AS e "
            "ON s.courseID = e.courseID "
            "AND s.secID = e.secID "
            "AND s.term = e.term),"

            "evalDept AS ("
            "SELECT e.evalID, i.deptID "
            "from instructor as i "
            "JOIN instructorEval as e "
            "ON i.userID = e.instructorID) "

            "SELECT evalID "
            "FROM evalDept "
            "WHERE deptID = %s;"
        )
    # run query using instructorID
    evalcursor.execute(queryEvalIDs, (dept,))
    # get results from query as list 
    evalIDs_list = [eval['evalID'] for eval in evalcursor.fetchall()]

    # convert evalIDs list to string
    evalIDs = ', '.join(evalIDs_list)
    # query for getting evaluation responses
    queryResponses = (
        "SELECT * "
        "FROM evalResponse "
        "WHERE evalID IN (%s) "
        "ORDER BY evalID"
    )
    # run query using evalIDs
    evalcursor.execute(queryResponses, (evalIDs,))
    # get results from query
    evalResponses = evalcursor.fetchall()

    # close DB and cursor
    evalcursor.close() 
    evalDB.close()

    if evalResponses:
        return evalResponses
    else:
        return "No evaluation responses found."


def getSpecEval(evalID: str, studentID: str) -> list[dict]:
    """ 
    Returns eval response of based on evalID.

    attrs: 
        evalID (str): id of evaluation
    return: 
        evalResponses (dict): a dict of evaluation responses of a given evaluation.
    """ 

    # open database connection
    evalDB = getDB()
    # cursor fetch will return as dict
    evalcursor = evalDB.cursor(dictionary=True)

    # query for db
    query = (
        "SELECT f.fieldID, f.title, e.response, e.created_at, e.last_modified "
        "FROM evalResponse AS e "
        "JOIN formField AS f "
        "ON e.evalID = e.evalID "
        "AND e.fieldID = f.fieldID "
        "WHERE e.studentID = %s " 
        "AND e.evalID = %s "
        "ORDER BY fieldID"
    )
    # run query using section IDs
    evalcursor.execute(query, (studentID, evalID,))
    # get results as dict
    evalResponses = evalcursor.fetchall()

    # close DB and cursor
    evalcursor.close() 
    evalDB.close()
    if evalResponses:
        return evalResponses
    else:
        return "No evaluation responses found."