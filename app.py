import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, send_file, url_for

from constants import ROLE
from database import (
    canViewRoster,
    getCourseDept,
    getCourseListDeptChair,
    getCourseListInstructor,
    getCourseListStudent,
    getCourseName,
    getDB,
    getEnrollmentId,
    getEvalListDeptChair,
    getEvalListInstructor,
    getEvalListStudent,
    getEvaluationFormInfo,
    getInstructorByCourse,
    getRoster,
    getSpecEval,
    getSubmittedStudents,
    getUserNameFromId,
    getUserRole,
    getUsersInfo,
    submitEvaluation,
)
from evaluation import getUniqueEvalList
from export import exportCSVCourse, exportXlsxCourse

app = Flask(__name__) 

load_dotenv()

PORT = os.getenv("PORT")

@app.route("/")
def index():
    return render_template('base.html')

@app.route("/homepage")
def homepage():
    return render_template("base.html")

# routes to the login page. dynamically generates user options for the dropdown
@app.route("/login")
def login():
    userData = getUsersInfo()
    return render_template("login.html", userData = userData)

# intermediary between /login & /home for proper handling of form data.
@app.route("/login-handler", strict_slashes = False, methods=['POST'])
def loginHandler():
    userID = request.form.get("userID")
    return redirect(url_for('home', userID=userID))

# where a user is brought to after a login attempt
@app.route("/home/<userID>")
def home(userID):

    # get all of the valid IDs
    userData = getUsersInfo()
    validUserIDS = [userData[i]["userID"] for i in range(len(userData))]

    # Gets the role of the user.
    userRole = getUserRole(userID)
    
    # checks if userID specified is valid
    if userID in validUserIDS:

        #get full name for displaying to the user
        userName = getUserNameFromId(userID)
        firstName = userName["firstName"]
        lastName = userName["lastName"]
        return render_template('homepage.html', userID = userID, firstName = firstName, lastName = lastName, userRole = userRole)
    else:
        # return error message; will appear if user attempts to type in url with an invalid userID
        return render_template("error.html", msg = "Error reaching homepage. User ID specified does not exist.")

# Student view for courses with evaluations to complete.
@app.route("/student/<userID>")
def student(userID):
    funny = "Time to evaluate your Professor 0.o" # I am laughter
    courseInfo = getCourseListStudent(userID) # gathers courses a student is in
    return render_template("studentEvalsToDo.html", msg = funny, userID = userID, courseInfo = courseInfo)

# Where students fill out an evaluation form for a selected class.
@app.route("/student/<userID>/eval-<courseID>-<secID>-<term>")
def evaluationPage(userID, courseID, secID, term):
    evaluationFormData = getEvaluationFormInfo(courseID, secID, term) # Get all the data associated with the evaluation & the fields

    # Gather additional information to prepare for form insertion into the database & for student viewing purposes
    evalID = evaluationFormData[0]["evalID"]
    instructorID = getInstructorByCourse(courseID, secID, term)
    instructorName = getUserNameFromId(instructorID)
    courseName = getCourseName(courseID)
    enrollID = getEnrollmentId(userID, courseID, secID, term)["enrollID"]
    fieldAmount = len(evaluationFormData) # The amount of fields an evaluation has

    return render_template("fillEvaluationPage.html", evaluationFormData = evaluationFormData, evalID = evalID, userID = userID, instructorName = instructorName, courseName = courseName, enrollID = enrollID, fieldAmount = fieldAmount)

# Evaluation submission page, regardless of whether insertion was successful or not
@app.route("/student/<userID>/evaluation-submission-handler", strict_slashes = False, methods=['POST'])
def evaluationSubmissionHandler(userID):
    # Gather the form data from the form submission
    formData = request.form.to_dict()

    # Splice the form data into easier-to-manage chunks. Will be used when adding form data to database.
    enrollID = formData["enrollID"]
    evalID = formData["evalID"]
    dateAndTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fieldAmount = int(formData["fieldAmount"]) # The amount of fields an evaluation has

    submissionStatus = "" # Will display to user whether form data was successfully submitted and added to the database
    for i in range(1, fieldAmount+1): # We look at each field in an evaluation
        fieldID = i
        currentField = f"field{fieldID}" # Will become "field1" for example; used to index the formData dict obtained from the form submission
        response = formData[currentField]
        submissionStatus = submitEvaluation(userID, response, dateAndTime, dateAndTime, enrollID, fieldID, evalID)
        if submissionStatus != "Your course evaluation form was submitted successfully! :D": # If something went wrong, we stop immediately and return an error message
            return render_template("studentEvalSubmission.html", formData = formData, userID = userID, submissionStatus = submissionStatus)

    # If nothing went wrong, we return a success message
    return render_template("studentEvalSubmission.html", formData = formData, userID = userID, submissionStatus = submissionStatus)

@app.route("/instructor")
def instructor(): 
    return "I hope they liked me (ᵕó_ò)"

@app.route("/admin")
def admin(): 
    return "Who's doing well ಠ_ಠ"


# just to test if app can connect to DBs
@app.route("/database-check")
def dbCheck(): 
    testdb = getDB()
    testcursor = testdb.cursor()
    query = "SELECT * FROM smithing;"
    print(query)
    testcursor.execute(query)
    DBresult_dict = testcursor.fetchall()
    testcursor.close()
    testdb.close()

    return f"DB: {DBresult_dict[0][0]}"

@app.route("/view-evals-list/<userID>", strict_slashes=False)
def viewEvaluationsList(userID):
    """Route for viewing evaluation list."""
    # check user type
    role = getUserRole(userID)

    if role == ROLE.instructor.value:
        # get eval responses
        evals = getEvalListInstructor(userID)
    elif role == ROLE.student.value:
        # get eval responses
        evals = getEvalListStudent(userID)
    elif role == ROLE.deptChair.value:
        # get eval responses
        evals = getEvalListDeptChair(userID)
    else:
        # render view for error
        return render_template(
            "error.html", 
            msg = ("That's weird. You have no role. " 
            "OR you're a school admin and that access "
            "is under construction."),
            userID = userID
            )

    # check if evals returned error message 
    if isinstance(evals, str):
        # render view for viewEvaluations with error msg
        return render_template(
            "viewEvaluationsList.html",  
            userID=userID,
            msg=evals
            )
    
    # get unique evaluations
    evals = getUniqueEvalList(evals)

    # render view for viewEvaluations
    return render_template(
        "viewEvaluationsList.html", 
        evals=evals, 
        userID=userID
        )


@app.route("/view-evals/<userID>/<studentID>/<evalID>", strict_slashes=False)
def viewEvaluation(studentID, evalID, userID):
    """Route for viewing evaluation responses."""
    # get fields for specific eval
    eval = getSpecEval(evalID, studentID)

    if isinstance(eval, str):
        # render view for viewEvaluations with error message
        return render_template(
            "viewEvaluation.html", 
            msg=eval,
            evalID=evalID,
            studentID=studentID,
            userID=userID
            )
    
    # get created timestamp
    created_at=eval[0]["created_at"]

    # get latest modified timestamp
    if [field["last_modified"] for field in eval if field["last_modified"]]:
        last_modified=max([field["last_modified"] for field in eval if field["last_modified"] is not None])
    else: last_modified = created_at

    # render view for viewEvaluations
    return render_template(
        "viewEvaluation.html", 
        eval=eval,
        last_modified=last_modified,
        created_at=created_at,
        evalID=evalID,
        studentID=studentID,
        userID=userID
        )

@app.route("/<userID>/view-roster/<courseID>/<secID>/<term>")
def viewRoster(userID, courseID, secID, term):
    """Route for viewing class roster."""
    # check if user can view roster
    if userID not in canViewRoster(courseID, secID, term):
        msg = (
            "Sorry looks like you do not have access to this roster.<br>"
            "Please try looking at a roster you have access to.<br>"
            "You can find rosters you have access to in "
            '"'
            f'<a href="{url_for("viewCourseList", userID=userID)}">'
            "VIEW COURSE LIST</a>"
            '"'
        )
        return render_template(
            "viewRoster.html", 
            userID = userID,
            msg = msg,
            courseID = courseID,
            secID = secID,
            term = term
            )

    # get the roster
    roster = getRoster(secID, courseID, term)

    # check if roster returned error message
    if isinstance(roster, str):
        return render_template(
            "viewRoster.html",
            userID = userID,
            msg = roster,
            courseID = courseID,
            secID = secID,
            term = term
        )
    
    evalID = f"{getCourseDept(courseID)}-{courseID}-{secID}-{term}"
    submittedStudents = getSubmittedStudents(roster, evalID)

    # render view of class roster
    return render_template(
        "viewRoster.html",
        roster = roster,
        courseID = courseID,
        secID = secID,
        term = term,
        submittedStudents = submittedStudents,
        evalID = evalID,
        userID = userID
    )

@app.route("/<userID>/view-courses", strict_slashes=False)
def viewCourseList(userID):
    """Route for viewing courses associated with a specific user."""

    # get user name
    name = getUserNameFromId(userID)

    # check user type
    role = getUserRole(userID)

    if role == ROLE.instructor.value:
        # get course list info
        courses = getCourseListInstructor(userID)
    elif role == ROLE.student.value:
        # get course list info
        courses = getCourseListStudent(userID)
    elif role == ROLE.deptChair.value:
        # get course list info
        courses = getCourseListDeptChair(userID)
    else:
        # render view for error
        return render_template(
            "error.html", 
            msg = ("That's weird. You have no role. " 
            "OR you're a school admin and that access "
            "is under construction."),
            userID = userID
            )

    # check if courses returned error message 
    if isinstance(courses, str):
        # render view for courseList with error msg
        return render_template(
            "courseList.html",  
            userID=userID,
            msg=courses,
            name=name
            )
    
    return render_template(
        "courseList.html", 
        courses=courses,
        name=name, 
        userID=userID,
        role=role
    )

@app.route("/<userID>/export/csv/<courseID>-<secID>-<term>/", strict_slashes=False)
def exportCSV(userID, courseID, secID, term):
    """export evaluation information to zip file with CSVs."""
    output, filename = exportCSVCourse(courseID, secID, term)

    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype='application/zip'
    )

@app.route("/<userID>/export/xlsx/<courseID>-<secID>-<term>/", strict_slashes=False)
def exportXlsx(userID, courseID, secID, term):
    """export evaluation information to an excel file."""
    output, filename = exportXlsxCourse(courseID, secID, term)

    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == "__main__": 
    app.run(debug=True, use_reloader=False, port=PORT)

'''
I believe y'all just need to run the following in the terminal of your cloned repository to access the virtual environment: 
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python app.py 
'''