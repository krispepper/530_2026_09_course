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

    args: 
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

    args: 
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
        
    argss: 
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

def getRoster(secID: int, courseID: int, term: str) -> list[dict]:
    """
    Function returns a dict with students attending a given class.
        
    argss: 
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
        "WITH enrollStudents AS ("
            "SELECT u.userID, u.firstName, u.lastName, u.email, e.enrollID "
            "FROM user AS u "
            "JOIN enrollment AS e "
            "ON e.studentID = u.userID "
            "WHERE e.secID = %s "
            "AND e.courseID = %s AND e.term = %s" \
        ") SELECT s.userID, s.studentID, es.firstName, es.lastName, es.email, IFNULL(ev.status, 'Not Started') AS status "
        "FROM enrollStudents AS es "
        "JOIN student AS s "
        "ON es.userID = s.userID "
        "LEFT JOIN evaluationStatus AS ev "
        "ON es.enrollID = ev.enrollID;"
        )
    # run query
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

def canViewRoster(courseID: int, secID: int, term: str) -> tuple:
    """
    Function returns a list with the userIDs of the class instructor and dept chair
        
    args: 
        secID (int): id of section for class
        courseID (int): id of course for class
        term (int): term for class (format: F or S followed by last two digits of year ex: F26)
    return: 
        allowedAccess(tuple): list of userID of instructor of course and dept chair 
    """
    # open database connection
    userDB = getDB()
    # cursor fetch will return as dict
    usercursor = userDB.cursor()

    # query for instructor and dept chair related to a class
    query = (
        "WITH courseSec AS ("
        "SELECT s.instructorID, s.courseID, s.secID, s.term, c.deptID "
        "FROM sections AS s "
        "JOIN courses AS c "
        "ON c.courseID = s.courseID" 
        ") "
        "SELECT d.chair, cs.instructorID "
        "FROM courseSec AS cs "
        "JOIN dept AS d "
        "ON d.ID = cs.deptID "
        "WHERE cs.courseID = %s " 
        "AND cs.secID = %s " 
        "AND cs.term = %s"
    )
    # run query using userID
    usercursor.execute(query, (courseID, secID, term))

    # get results as dict
    allowedAccess_DB= usercursor.fetchone()

    # check if none returned
    if not allowedAccess_DB:
        # return empty list if no instructors found
        return []

    # tuple of instructor and dept chair userIDs what can view roster
    return allowedAccess_DB

def getSubmittedStudents(roster: list[dict], evalID: str) -> list:
    """
    Function gets list of students who have submitted IDs
        
    args: 
        roster (list[dict]): roster of students in a class (from getRoster)
        evalID (str): evaluation ID for the class
    return: 
        submittedStudents (list): list of students in a class who have submitted an evaluation.
    """
    # open database connection
    userDB = getDB()
    # cursor fetch will return as dict
    usercursor = userDB.cursor()

    # check if roster is empty
    if roster == [{}]:
        submittedStudents = []
    else:
        # get list of studentIDs
        studentIDs = [s["userID"] for s in roster]
        # make placeholders
        placeholders = ", ".join(["%s"]*len(roster))

        # query
        query = (
            "SELECT DISTINCT (er.studentID)"
            "FROM evalResponse AS er "
            "JOIN evaluationStatus AS es "
            "ON er.enrollID = es.enrollID "
            "AND er.evalID = es.evalID "
            f"WHERE er.evalID = '{evalID}' "
            f"AND er.studentID in ({placeholders})"
            "AND es.status = 'Completed'"
        )
        # run query using instructorID
        usercursor.execute(query, tuple(studentIDs))

        # get results as dict
        subEvals = usercursor.fetchall()

        # turn into list
        submittedStudents = [s[0] for s in subEvals] 

    # list of students userIDs that have submitted evals
    return submittedStudents

def getInstructorByCourse(courseID: int, secID: int, term: str) -> str:
    """
    Function returns userID of an instructor for a given class
       
    argss: 
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
    if instructorInfo and instructorInfo["instructorID"] != None: 
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
    
    argss: 
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

    # check if no evalIDs were found
    if not evalIDs_list:
        return "No evaluation responses found."

    # make placeholders
    placeholders = ", ".join(["%s"]*len(evalIDs_list))

    # query for getting evaluation responses
    queryResponses = (
        "SELECT * "
        "FROM evalResponse "
        f"WHERE evalID IN ({placeholders}) "
        "ORDER BY evalID"
    )
    # run query using evalIDs
    evalcursor.execute(queryResponses, tuple(evalIDs_list))

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

def getEvalListStudent(studentID: str) -> list[dict]:
    """ 
    Function returns a dict with eval responses associated with a given student.
    
    argss: 
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

    # if empty return error message
    if all(evalResponse == {} for evalResponse in evalResponses):
            return "No evaluation responses found."

    # else return eval responses
    return evalResponses

def getEvalListDeptChair(deptChairID: str) -> list[dict]:
    """ 
    Function returns a dict with evaluation responses associated with a given department chair.
    
    argss: 
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

    # check if no evalIDs were found
    if not evalIDs_list:
        return "No evaluation responses found."

    # make placeholders
    placeholders = ", ".join(["%s"]*len(evalIDs_list))

    # query for getting evaluation responses
    queryResponses = (
        "SELECT * "
        "FROM evalResponse "
        f"WHERE evalID IN ({placeholders}) "
        "ORDER BY evalID"
    )
    # run query using evalIDs
    evalcursor.execute(queryResponses, tuple(evalIDs_list))
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
    
    argss: 
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

    argss: 
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
        "ON e.evalID = f.evalID "
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
    
    # if empty return error message
    if all(evalResponse == {} for evalResponse in evalResponses):
            return "No evaluation responses found."

    # else return eval responses
    return evalResponses

# COURSE FUNCTIONS
def getCourseName(courseID: int) -> str:
    """
    Function returns a information about an given class
       
    argss: 
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
        
    argss: 
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
        
    argss: 
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
        
    argss: 
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
        # add column for if evaluations exist
        for course in courses:
            if isinstance(getEvalByClass(course["courseID"], course["secID"], course["term"]), str):
                course["hasEval"] = False
            else:
                course["hasEval"] = True
        # return list of courses
        return courses

def getCourseListDeptChair(userID: str) -> list[dict]:
    """
    Function returns a list of course information for a given instructor.
        
    argss: 
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
        # add column for if evaluations exist
        for course in courses:
            if isinstance(getEvalByClass(course["courseID"], course["secID"], course["term"]), str):
                course["hasEval"] = False
            else:
                course["hasEval"] = True
        # return list of courses
        return courses

# Gets the information from an evaluation form & its fields.
# Takes parameters courseID, secID (sectionID), and term)
# returns the evaluationID, title of the field, type of the field, the ID of the field, the options (if any), and the filed subject.
def getEvaluationFormInfo(courseID, secID, term) -> str:
    # establish DB connection & define cursor
    userDB = getDB()
    usercursor = userDB.cursor(dictionary=True)

    # query that gathers the return info based on the parameters.
    query = "select evaluation.evalID, formField.title, formField.fieldType, formField.fieldID, formField.options, formField.fieldSubject from evaluation inner join formField on (evaluation.evalID = formField.evalID) INNER JOIN sections ON (evaluation.courseID = sections.courseID AND evaluation.secID = sections.secID AND evaluation.term = sections.term) WHERE evaluation.courseID = %s AND evaluation.secID = %s AND evaluation.term = %s;"


    usercursor.execute(query, (courseID, secID, term,))
    DBresult_array = usercursor.fetchall() # get all the data

    # close everything
    usercursor.close() 
    userDB.close()

    # Ensure we actually retrieved data.
    if len(DBresult_array) != 0:
        return DBresult_array # array of JSON
    else:
        return "Data not found."

# Gets the enrollmentID of a student.
# Takes the student's ID, the courseID, secID (sectionID), and the term.
def getEnrollmentId(studentID, courseID, secID, term) -> str:
    # establish DB connection
    userDB = getDB()
    usercursor = userDB.cursor(dictionary=True)

    # query; a simple selection based on the parameters
    query = 'SELECT enrollID FROM enrollment WHERE studentID = %s AND courseID = %s AND secID = %s AND term = %s;'
    usercursor.execute(query, (studentID, courseID, secID, term,))
    DBresult_dict = usercursor.fetchone() # fetchOne since there will only be 1 result we need; returned as dict, makes life easier

    # close DB and cursor
    usercursor.close() 
    userDB.close()

    # ensure the enrollment ID was actually found
    if DBresult_dict is not None:
        return DBresult_dict
    else:
        # return error message
        return "Enrollment ID not found."

# Insert function; adds the results of a student's evaluation form submission to the database
# Directly manipulates the evalResponse table. Parameters included are all of the fields for the evalResponse table (excluding evalResponseID column, since that one is auto increment)
# Returns either a success or failure message based on a try-catch block.
def submitEvaluation(studentID, response, created_at, last_modified, enrollID, fieldID, evalID) -> str:
    # establish DB connection
    userDB = getDB()
    usercursor = userDB.cursor(dictionary=True)

    # Insert query.
    query = 'INSERT INTO evalResponse (studentID, response, created_at, last_modified, enrollID, fieldID, evalID) VALUES (%s, %s, %s, %s, %s, %s, %s);'

    # With how sensitive insertions can be, you need a try-except block.
    try:
        usercursor.execute(query, (studentID, response, created_at, last_modified, enrollID, fieldID, evalID,)) # Stage database insert with execute.
        userDB.commit() # Actually change the database by using commit.

        # close DB and cursor
        usercursor.close() 
        userDB.close()

        return "Your course evaluation form was submitted successfully! :D"
    except Exception: # If ANYTHING goes wrong, roll back the changes & return error message.
        userDB.rollback()
        return "An error occured while submitting your course evaluation form. :'("