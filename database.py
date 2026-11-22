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

# Gets firstName, lastName, & userID from the user table.
def getUsersInfo() -> str:
    # establish DB connection & define cursor
    userDB = getDB()
    usercursor = userDB.cursor(dictionary=True)

    query = "SELECT firstName, lastName, userID FROM user;"

    usercursor.execute(query)
    DBresult_array = usercursor.fetchall() # get all the data

    # close everything
    usercursor.close() 
    userDB.close()

    return DBresult_array # array of JSON

# Gets firstName & lastName from user table given a specified userID
def getUserNameFromId(userID) -> str:

    # establish DB connection
    userDB = getDB()
    usercursor = userDB.cursor(dictionary=True)

    query = 'select firstName, lastName from user where userID = %s;'
    usercursor.execute(query, (userID,))
    DBresult_dict = usercursor.fetchone()

    # close DB and cursor
    usercursor.close() 
    userDB.close()

    # ensure the user was actually found
    if DBresult_dict is not None:
        return DBresult_dict
    else:
        # return error message
        return f"User not found with userID of: '{userID}'."

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

# so that course info is properly formatted
def getDeptAbbreviation(deptID: int) -> str:
    db = getDB()
    cursor = db.cursor(dictionary=True)

    query = "SELECT code FROM dept WHERE ID = %s"
    cursor.execute(query, (deptID,))
    result = cursor.fetchone()

    cursor.close()
    db.close()

    if result is not None:
        return result["code"]
    else:
        return f"No department abbreviation found for deptID '{deptID}'."


def getRoster(secID: int, courseID: int, term: str) -> list[dict]:
    """
    Function returns a dict with students attending a given class.
        
    attrs: 
        secID (int): id of section for class
        courseID (int): id of course for class
        term (int): term for class (format: F or S followed by last two digits of year ex: F26)
    return: 
        roster (list[dict]): list of students in a class.
    """
    # open database connection
    userDB = getDB()
    # cursor fetch will return as dict
    usercursor = userDB.cursor(dictionary=True)

    # query to get list of student information for a specific class
    query = (
        'With enrollStudents as ('
        'SELECT u.userID, u.firstName, u.lastName, u.email '
        'FROM user AS u '
        'JOIN enrollment AS e '
        'ON e.studentID = u.userID '
        'WHERE secID = %s '
        'AND courseID = %s '
        'AND term = %s) '
        'SELECT s.studentID, es.firstName, es.lastName, es.email '
        'FROM enrollStudents as es '
        'JOIN student as s '
        'ON es.userID = s.userID'
        )
    # run query using instructorID
    usercursor.execute(query, (secID, courseID, term))
    # get results as dict
    DBresult_dict = usercursor.fetchall()

    # check if any students were found
    if all(student == {} for student in DBresult_dict):

        # close DB and cursor
        usercursor.close() 
        userDB.close()
        

        # return error message
        return f"No enrollment found for course '{courseID}-{secID}-{term}'."

    # close DB and cursor
    usercursor.close() 
    userDB.close()

    # return role
    return DBresult_dict

def getInstructorByCourse(courseID: int, secID: int, term: str) -> str:
    """
    Function returns userID of an instructor for a given class
       
    attrs: 
        secID (int): id of section for class
        courseID (int): id of course for class
        term (int): term for class (format: F or S followed by last two digits of year ex: F26)
    return: 
        userID (str): userID for instructor teaching class
    """
    # open database connection
    userDB = getDB()
    # cursor fetch will return as dict
    usercursor = userDB.cursor(dictionary=True)

    # query for db
    query = (
        "SELECT instructorID "
        "FROM sections "
        "WHERE courseID=%s AND secID=%s AND term=%s" 
    )
    # run query using instructorID
    usercursor.execute(query, (courseID, secID, term))
    # get results as dict
    instructorInfo = usercursor.fetchone()


    # close DB and cursor
    usercursor.close() 
    userDB.close()

    # check user was found
    if instructorInfo: 
        # return instructor info
        userID = instructorInfo["instructorID"]
        return userID
    else:
        # return error message 
        return f"No instructor found for {courseID}-{secID}-{term}."


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

    # if empty return error message
    if all(evalResponse == {} for evalResponse in evalResponses):
            return "No evaluation responses found."

    # else return eval responses
    return evalResponses


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

    # if empty return error message
    if all(evalResponse == {} for evalResponse in evalResponses):
            return "No evaluation responses found."

    # else return eval responses
    return evalResponses

def getEvalByClass(courseID: int, secID: int, term: str) -> list[dict]:
    """ 
    Function returns a dict with evaluation responses associated with a given class.
    
    attrs: 
        secID (int): id of section for class
        courseID (int): id of course for class
        term (int): term for class (format: F or S followed by last two digits of year ex: F26)
    return: 
        a dict of evaluation responses associated with a given dept chair.
    """
    # open database connection
    evalDB = getDB()
    # cursor fetch will return as dictionary
    evalcursor = evalDB.cursor(dictionary=True)

    # query for getting evalIDs
    queryEvalIDs = (
         "WITH evals AS ("
         "SELECT e.*, f.title, f.fieldSubject "
         "FROM evalResponse AS e "
         "JOIN formField AS f "
         "ON e.evalID = f.evalID "
         "AND e.fieldID = f.fieldID), "
         "evalCourse AS ("
         "SELECT ev.*, e.courseID, e.secID, e.term "
         "FROM evals AS ev "
         "JOIN evaluation AS e "
         "ON ev.evalID = e.evalID " 
         "WHERE courseID = %s AND secID = %s AND term = %s) "
         "SELECT * from evalCourse" 
        )
    # run query using instructorID
    evalcursor.execute(queryEvalIDs, (courseID, secID, term))
    # get results from query as list 
    evalResponses = evalcursor.fetchall()

    # close DB and cursor
    evalcursor.close() 
    evalDB.close()

    # if empty return error message
    if all(evalResponse == {} for evalResponse in evalResponses):
         return f"No evaluation responses found for {courseID}-{secID}-{term}."

    # else return eval responses
    return evalResponses

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
    # I swapped the order of formField and evalResponse because we want to ensure all questions are returned.
    query = (
        "SELECT f.fieldID, f.title, e.response, e.created_at, e.last_modified "
        "FROM formField AS f "
        "LEFT JOIN evalResponse AS e "
        "ON f.evalID = e.evalID "
        "AND f.fieldID = e.fieldID "
        "AND e.studentID = %s " 
        "WHERE f.evalID = %s "
        "ORDER BY f.fieldID"
    )
    # run query using section IDs
    evalcursor.execute(query, (studentID, evalID,))
    # get results as dict
    evalResponses = evalcursor.fetchall()

    # close DB and cursor
    evalcursor.close() 
    evalDB.close()
    
    # if empty return error message # may have to come back and fix this part 
    if all(evalResponse == {} for evalResponse in evalResponses):
            return "No evaluation responses found."

    # else return eval responses
    return evalResponses

# COURSE FUNCTIONS
def getCourseName(courseID: int) -> str:
    """
    Function returns a information about an given class
       
    attrs: 
        courseID (int): id of course for class
    return: 
        courseName (str): name of course
    """
    # open database connection
    courseDB = getDB()
    # cursor fetch will return as dict
    coursecursor = courseDB.cursor(dictionary=True)

    # query for db
    query = (
        "SELECT name "
        "FROM courses "
        "WHERE courseID=%s" 
    )
    # run query 
    coursecursor.execute(query, (courseID,))
    # get results as dict
    DBresult_dict = coursecursor.fetchone()

    # close DB and cursor
    coursecursor.close() 
    courseDB.close()

    # check course was found
    if DBresult_dict: 
        # return course name
        courseName = DBresult_dict["name"]
        return courseName
    else:
        # return error message 
        return f"No course name found for {courseID}."

def getCourseDept(courseID: int) -> str:
    """
    Function returns a course's department
        
    attrs: 
        courseID (int): id of course for class
    return: 
        dept (str): name of dept
    """
    # open database connection
    courseDB = getDB()
    # cursor fetch will return as dict
    coursecursor = courseDB.cursor(dictionary=True)

    # query for db
    query = (
        "SELECT code "
        "FROM dept AS d "
        "JOIN courses AS c "
        "ON c.deptID = d.ID "
        "WHERE c.courseID=%s" 
    )
    # run query using courseID
    coursecursor.execute(query, (courseID, ))
    # get results as dict
    DBresult_dict = coursecursor.fetchone()

    # close DB and cursor
    coursecursor.close() 
    courseDB.close()

    # check course dept was found
    if DBresult_dict: 
        # return course dept code
        dept = DBresult_dict["code"]
        return dept
    else:
        # return error message 
        return f"No dept id for course {courseID}."

def getCourseListStudent(userID: str) -> list[dict]:
    """
    Function returns a list of course information for a given student.
        
    attrs: 
        userID (str): id of user
    return: 
        courses (list[dict]): course information (name, course, sec, term) for courses of a student 
    """
    
    # get user name
    userName = getUserNameFromId(userID)

    # open database connection
    courseDB = getDB()
    # cursor fetch will return as dict
    coursecursor = courseDB.cursor(dictionary=True)

    # query for db
    query = (
        "WITH courseInfo AS ("
        "SELECT c.name, s.courseID, s.secID, s.term "
        "FROM courses as c "
        "JOIN sections as s "
        "ON c.courseID = s.courseID) "
        "SELECT ci.* "
        "FROM courseInfo AS ci "
        "JOIN enrollment AS e "
        "ON ci.courseID = e.courseID "
        "AND ci.secID = e.secID "
        "AND ci.term = e.term "
        "WHERE e.studentID = %s"
    )
    # run query using userID
    coursecursor.execute(query, (userID, ))
    # get results as dict
    courses = coursecursor.fetchall()

    # close DB and cursor
    coursecursor.close() 
    courseDB.close()

    # check if courses were found
    if all(course == {} for course in courses):
        # return error message 
        return f"No courses found for {userName["firstName"]} {userName["lastName"]}."
    else:
        # return list of courses
        return courses
        
def getCourseListInstructor(userID: str) -> list[dict]:
    """
    Function returns a list of course information for a given instructor.
        
    attrs: 
        userID (str): id of user
    return: 
        courses (list[dict]): course information (name, course, sec, term) for courses of an instructor 
    """

    # get user name
    userName = getUserNameFromId(userID)

    # open database connection
    courseDB = getDB()
    # cursor fetch will return as dict
    coursecursor = courseDB.cursor(dictionary=True)

    # query for db
    query = (
        "SELECT c.name, s.courseID, s.secID, s.term "
        "FROM courses as c "
        "JOIN sections as s "
        "ON c.courseID = s.courseID "
        "WHERE s.instructorID = %s"
    )
    # run query using userID
    coursecursor.execute(query, (userID, ))
    # get results as dict
    courses = coursecursor.fetchall()

    # close DB and cursor
    coursecursor.close() 
    courseDB.close()

    # check if courses were found
    if all(course == {} for course in courses):
        # return error message 
        return f"No courses found for {userName["firstName"]} {userName["lastName"]}."
    else:
        # return list of courses
        return courses

def getCourseListDeptChair(userID: str) -> list[dict]:
    """
    Function returns a list of course information for a given instructor.
        
    attrs: 
        userID (str): id of user
    return: 
        courses (list[dict]): course information (name, course, sec, term) for courses of an instructor 
    """

    # get dept 
    dept = getDept(userID)

    # get user name
    userName = getUserNameFromId(userID)

    # open database connection
    courseDB = getDB()
    # cursor fetch will return as dict
    coursecursor = courseDB.cursor(dictionary=True)

    # query for db
    query = (
        "SELECT c.name, s.courseID, s.secID, s.term "
        "FROM courses as c "
        "JOIN sections as s "
        "ON c.courseID = s.courseID "
        "WHERE c.deptID = %s"
    )
    # run query using userID
    coursecursor.execute(query, (dept, ))
    # get results as dict
    courses = coursecursor.fetchall()

    # close DB and cursor
    coursecursor.close() 
    courseDB.close()

    # check if courses were found
    if all(course == {} for course in courses):
        # return error message 
        return f"No courses found for {userName["firstName"]} {userName["lastName"]}."
    else:
        # return list of courses
        return courses

# Create a User (role identified ties the user to their respective table)
def createUser(userID, firstName, lastName, email, role): 
    db = getDB()
    cursor = db.cursor()

    query = """INSERT INTO `user` (userID, firstName, lastName, email, role) 
    VALUES (%s, %s, %s, %s, %s)"""
    values = (userID, firstName, lastName, email, role) 

    cursor.execute(query, values)
    db.commit()

    cursor.close()
    db.close() 

# Add (like an import) 10 Standard Questions (these are on every form) to the database 
def add_standardQuestions(eval_ID): 
    db = getDB()
    cursor = db.cursor()

    query = """INSERT INTO formField (fieldID,evalID, title, fieldType, fieldSubject, options) 
    VALUES (%s, %s, %s, %s, %s, %s)"""

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

def createEvaluation(evalID, creator, secID, courseID, term, customName, deadline):
    db = getDB()
    cursor = db.cursor()

    query = """INSERT INTO evaluation (evalID, creator, secID, courseID, term, customName, deadline)
    VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    cursor.execute(query, (evalID, creator, secID, courseID, term, customName, deadline))
    db.commit()

    add_standardQuestions(evalID)

    cursor.close()
    db.close()

    return evalID

# Pull the questions for the web app 
def getEvalQuestions(evalID: str) -> list[dict]:
    """ 
    Returns all questions associated with a given evaluation.
    attributes: 
        evalID (str): ID of evaluation
    return: 
        questions 
    (list[dict]): All questions for the evaluation.
    """

    evalDB = getDB()
    evalcursor = evalDB.cursor(dictionary=True)

    # Query for database
    query = ( "SELECT fieldID, title, fieldType, fieldSubject, options " "FROM formField "
        "WHERE evalID = %s " "ORDER BY fieldID")

    evalcursor.execute(query, (evalID,))

    # Get results as dictionaries
    questions = evalcursor.fetchall()

    evalcursor.close()
    evalDB.close()

    # Return error message if no questions found
    if not questions:
        return "No evaluation questions found."

    return questions

# Allow students to save questions they filled out 
def saveEvalResponse(studentID, enrollID, evalID, fieldID, response):
    """
    Inserts a new student response or updates an existing response.
    """

    evalDB = getDB()
    evalcursor = evalDB.cursor()

    query = ( "SELECT evalResponseID FROM evalResponse " 
    "WHERE enrollID = %s AND evalID = %s AND fieldID = %s")

    evalcursor.execute(query, (enrollID, evalID, fieldID))
    existingResponse = evalcursor.fetchone()

    if existingResponse:
        query = ("UPDATE evalResponse SET response = %s, last_modified = CURRENT_TIMESTAMP "
            "WHERE evalResponseID = %s")
        evalcursor.execute(query, (response, existingResponse[0]))

    else:
        query = ( "INSERT INTO evalResponse (studentID, enrollID, evalID, fieldID, response, created_at) "
            "VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)")
        evalcursor.execute( query, (studentID, enrollID, evalID, fieldID, response) )

    evalDB.commit()

    evalcursor.close()
    evalDB.close()

# Saves the new status of the evaluation (Not Started, In Progress, Completed)
def saveEvalStatus(enrollID: int, evalID: str, status: str):
    """
    Inserts or updates the status of a student's evaluation.
    attrs:
        enrollID (int): Student enrollment ID
        evalID (str): Evaluation ID
        status (str): Not Started, In Progress, or Completed
    """

    evalDB = getDB()
    evalcursor = evalDB.cursor()

    query = ( "INSERT INTO evaluationStatus (enrollID, evalID, status) VALUES (%s, %s, %s) "
        "ON DUPLICATE KEY UPDATE status = VALUES(status)")

    evalcursor.execute(query, (enrollID, evalID, status))
    evalDB.commit()

    evalcursor.close()
    evalDB.close()

def getEvalListStudent(studentID: str) -> list[dict]:
    """
    Returns all evaluations assigned to a student, including their current status.
    attrs:
        studentID (str): ID of student
    return:
        evalList (list[dict]): List of assigned evaluations
    """

    evalDB = getDB()

    # fetch 
    evalcursor = evalDB.cursor(dictionary=True)

    query = (
        "SELECT enrol.studentID, eval.evalID, enrol.courseID, enrol.secID, enrol.term, enrol.enrollID, eval.deadline, "
        "COALESCE(ev_st.status, 'Not Started') AS status, CASE "
        "WHEN eval.deadline IS NOT NULL AND eval.deadline < NOW() "
        "AND COALESCE(ev_st.status, 'Not Started') != 'Completed' "
        "THEN 'Past Due' "
        "ELSE COALESCE(ev_st.status, 'Not Started') "
        "END AS displayStatus "
        "FROM enrollment AS enrol JOIN evaluation AS eval "
        "ON enrol.courseID = eval.courseID AND enrol.secID = eval.secID AND enrol.term = eval.term "
        "LEFT JOIN evaluationStatus AS ev_st ON enrol.enrollID = ev_st.enrollID AND eval.evalID = ev_st.evalID "
        "WHERE enrol.studentID = %s ORDER BY eval.evalID"
    )

    evalcursor.execute(query, (studentID,))

    # get results as dict
    evalList = evalcursor.fetchall()

    evalcursor.close()
    evalDB.close()

    # if empty return error message
    if not evalList:
        return "No evaluation responses found."
    return evalList

# Retrieves the evaluation status (for web app)
def getEvalStatus(enrollID: int, evalID: str) -> str:
    """
    Returns the current status of a student's evaluation.
    """
    evalDB = getDB()
    evalcursor = evalDB.cursor(dictionary=True)

    query = ( "SELECT status " "FROM evaluationStatus " "WHERE enrollID = %s AND evalID = %s")

    evalcursor.execute(query, (enrollID, evalID))
    status = evalcursor.fetchone()

    evalcursor.close()
    evalDB.close()

    if status:
        return status["status"]

    return "Not Started"


# Pull the student responses 
def getEvalResponses(enrollID: int, evalID: str) -> list[dict]:
    """
    Returns previously saved responses for a student evaluation.
    """

    evalDB = getDB()
    evalcursor = evalDB.cursor(dictionary=True)

    query = ( "SELECT fieldID, response FROM evalResponse "
        "WHERE enrollID = %s AND evalID = %s ORDER BY fieldID")

    evalcursor.execute(query, (enrollID, evalID))
    evalResponses = evalcursor.fetchall()

    evalcursor.close()
    evalDB.close()

    return evalResponses

# Edit Evaluation Form 
def edit_evaluationQuestion(eval_ID, field_ID, title, fieldType, fieldSubject, options):
    db = getDB() 
    cursor = db.cursor() 

    query = """UPDATE formField SET title = %s, fieldType = %s, fieldSubject=%s, options = %s 
    WHERE evalID = %s AND fieldID = %s"""
    values = (title, fieldType, fieldSubject, options, eval_ID, field_ID)

    cursor.execute(query,values)
    db.commit()

    updatedQuestion = cursor.rowcount

    cursor.close()
    db.close()

    return updatedQuestion

# Ensure Past Due evaluations cannot be edited. 
def isEvaluationPastDue(evalID: str) -> bool:
    db = getDB()
    cursor = db.cursor(dictionary=True)

    query = ( "SELECT deadline IS NOT NULL AND deadline < NOW() AS pastDue " 
    "FROM evaluation WHERE evalID = %s" )

    cursor.execute(query, (evalID,))
    result = cursor.fetchone()

    cursor.close()
    db.close()

    return bool(result["pastDue"]) if result else False

def getEnrollmentByID(enrollID: int) -> dict:
    """
    Returns enrollment information for a given enrollment ID.
    """
    evalDB = getDB()
    evalcursor = evalDB.cursor(dictionary=True)

    # query for enrollment
    query = ( "SELECT studentID, courseID, secID, term " "FROM enrollment " "WHERE enrollID = %s")

    evalcursor.execute(query, (enrollID,))
    enrollment = evalcursor.fetchone()

    evalcursor.close()
    evalDB.close()

    return enrollment
