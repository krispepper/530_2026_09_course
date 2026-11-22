import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, send_file, url_for

from constants import ROLE
from database import (
    getCourseListDeptChair,
    getCourseListInstructor,
    getCourseListStudent,
    getDB,
    getEvalListDeptChair,
    getEvalListInstructor,
    getEvalListStudent,
    getRoster,
    getSpecEval,
    getUserNameFromId,
    getUserRole,
    getUsersInfo,
    getEnrollmentByID,
    getEvalQuestions,
    getEvalResponses,
    getEvalStatus,
    saveEvalResponse,
    saveEvalStatus,
    createEvaluation,
    getDept,
    getDeptAbbreviation, 
    isEvaluationPastDue,
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
    
    # checks if userID specified is valid
    if userID in validUserIDS:

        #get full name for displaying to the user
        userName = getUserNameFromId(userID)
        firstName = userName["firstName"]
        lastName = userName["lastName"]

        role = getUserRole(userID)
        isDeptChair = role == ROLE.deptChair.value

        return render_template('homepage.html', userID = userID, firstName = firstName, lastName = lastName, isDeptChair=isDeptChair)
   
    else:
        # return error message; will appear if user attempts to type in url with an invalid userID
        return render_template("error.html", msg = "Error reaching homepage. User ID specified does not exist.")

@app.route("/student")
def student(): 
    return "Time to evaluate your Professor 0.o"

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

# Using jsonify so there is a meaningful HTTP response
@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()

    userID = data.get("userID")
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email = data.get("email")
    role = data.get("role")

    if not all([userID, firstName, lastName, email, role]): 
        return jsonify({"error":"All fields must be completed"}), 400 

    if role not in ["stu", "ins", "sca", "dc"]:
        return jsonify({"error": "Invalid role"}), 400

    # Using regular expression so that we are checking for the pattern of @
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify({"error": "Invalid email"}), 400

    createUser(userID, firstName, lastName, email, role)

    return jsonify({"message": "User was successfully created"}), 201

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
            "is under construction.")
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
    #evals = getUniqueEvalList(evals)

    # render view for viewEvaluations
    return render_template(
        "viewEvaluationsList.html", 
        evals=evals, 
        userID=userID
        )

@app.route("/<userID>/create-evaluation", methods=["GET", "POST"])
def createEvaluationForm(userID):

    # check if user is a department chair
    if getUserRole(userID) != ROLE.deptChair.value:
        return render_template("error.html", msg="Access denied.")

    # get courses for the department chair
    courses = getCourseListDeptChair(userID)

    if request.method == "POST":
        creator = userID

        # get selected course information
        selectedSection = request.form["section"]
        courseID, secID, term = selectedSection.split("|")

        # generate evaluation ID
        # get department abbreviation
        dept = getDept(userID)
        deptAbbrev = getDeptAbbreviation(dept)

        evalID = f"{deptAbbrev}-{courseID}-{secID}-{term}"

        customName = request.form["customName"]
        deadline = request.form["deadline"]

        if deadline == "":
            deadline = None

        createEvaluation( evalID, creator, secID, courseID, term, customName, deadline)

        return redirect(url_for("home", userID=userID))

    return render_template(
        "createEvaluation.html",
        userID=userID,
        courses=courses,
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
    
    # I edited this so that we prevent crashing if there are no dates and returns None if there isn't one. 
    # get lastest modified timestamp
    last_modified = max( [field["last_modified"] for field in eval if field["last_modified"] is not None],
        default=None )
    # get created timestamp
    created_at=next( (field["created_at"] for field in eval if field["created_at"] is not None),
        None )

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

# Open an evaluation 
@app.route("/<userID>/evaluate/<enrollID>/<evalID>", methods=["GET"])
def completeEvaluation(userID, enrollID, evalID):

    # Get enrollment information
    enrollment = getEnrollmentByID(enrollID)

    if not enrollment:
        return render_template( "completeEvaluation.html", msg="Enrollment not found.")

    courseID = enrollment["courseID"]
    studentID = enrollment["studentID"]

    # Get current evaluation status
    status = getEvalStatus(enrollID, evalID)
    pastDue = isEvaluationPastDue(evalID) # Check whether the evaluation deadline has passed

    # Update status if evaluation has not been completed
    if status == "Not Started" and not pastDue:
        saveEvalStatus(enrollID, evalID, "In Progress")
        status = "In Progress"

    # Get evaluation questions and saved responses
    questions = getEvalQuestions(evalID)
    responses = getEvalResponses(enrollID, evalID)

    return render_template(
        "completeEvaluation.html",
        courseID=courseID,
        studentID=studentID,
        status=status,
        pastDue=pastDue,
        msg=None,
        questions=questions,
        responses=responses,
        userID=userID,
        enrollID=enrollID,
        evalID=evalID
    )

# Save progress of evaluation 
@app.route("/<userID>/evaluate/<enrollID>/<evalID>/save",methods=["POST"])
def saveProgress(userID, enrollID, evalID):

    if isEvaluationPastDue(evalID):
        return redirect(url_for("viewEvaluationsList", userID=userID))

    if getEvalStatus(enrollID, evalID) == "Completed":
        return redirect(url_for("viewEvaluationsList", userID=userID))

    # Get enrollment information to retrieve studentID
    enrollment = getEnrollmentByID(enrollID)
    if not enrollment:
        return redirect(url_for("viewEvaluationsList", userID=userID))

    studentID = enrollment["studentID"]

    # Check current status before updating
    current_status = getEvalStatus(enrollID, evalID)

    # Iterate through submitted answers
    for fieldID, response in request.form.items():
        # Skip the action button so "save"/"submit" is not stored as an answer
        if fieldID == "action":
            continue

        # Save each answer
        saveEvalResponse(studentID, enrollID, evalID, fieldID, response)

    # Only update status if not already completed
    if current_status != "Completed":
        saveEvalStatus(enrollID, evalID, "In Progress")

    return redirect( url_for("completeEvaluation", userID=userID, enrollID=enrollID, evalID=evalID) )

# Submit an application (marks it as complete)
@app.route("/<userID>/evaluate/<enrollID>/<evalID>/submit",methods=["POST"])
def submitEvaluation(userID, enrollID, evalID):

    if isEvaluationPastDue(evalID):
        return redirect(url_for("viewEvaluationsList", userID=userID))

    if getEvalStatus(enrollID, evalID) == "Completed":
        return redirect(url_for("viewEvaluationsList", userID=userID))

    # Get enrollment information to retrieve studentID
    enrollment = getEnrollmentByID(enrollID)
    if not enrollment:
        return redirect(url_for("viewEvaluationsList", userID=userID))

    studentID = enrollment["studentID"]

    # Save the latest answers
    for fieldID, response in request.form.items():
        # Skip the action button so "save"/"submit" is not stored as an answer
        if fieldID == "action":
            continue
        saveEvalResponse(studentID, enrollID, evalID, fieldID, response)

    # Mark evaluation as completed
    saveEvalStatus(enrollID, evalID, "Completed")

    return redirect( url_for("viewEvaluationsList",userID=userID) )

@app.route("/view-roster/<courseID>/<secID>/<term>")
def viewRoster(courseID, secID, term):
    """Route for viewing class roster."""
    # get the roster
    roster = getRoster(secID, courseID, term)

    # render view of class roster
    return render_template(
        "viewRoster.html",
        roster = roster,
        courseID = courseID,
        secID = secID,
        term = term
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
            "is under construction.")
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