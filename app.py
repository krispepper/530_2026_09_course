import os

from dotenv import load_dotenv
from flask import Flask, render_template

from database import (
        getDB, 
        getEvalListInstructor, 
        getEvalListStudent, 
        getEvalListDeptChair,  
        getUserRole,
        getUniqueEvalList,
        getSpecEval
    )
from constants import ROLE

app = Flask(__name__) 

load_dotenv()

PORT = os.getenv("PORT")

@app.route("/")
def index():
    return render_template('base.html')

@app.route("/homepage")
def home(): 
    return render_template('base.html')

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
    query = "SELECT * FROM smithing"
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
        evals = getUniqueEvalList(getEvalListInstructor(userID))
    elif role == ROLE.student.value:
        # get eval responses
        evals = getUniqueEvalList(getEvalListStudent(userID))
        print(evals)
    elif role == ROLE.deptChair.value:
        # get eval responses
        evals = getUniqueEvalList(getEvalListDeptChair(userID))
    else:
        return render_template(
            "error.html", 
            msg = ("That's weird. You have no role. " 
            "OR you're a school admin and that access "
            "is under construction.")
            )

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

    # get lastest modified timestamp
    last_modified=max([field["last_modified"] for field in eval])
    # get created timestamp
    created_at=eval[0]["created_at"]

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


if __name__ == "__main__": 
    app.run(debug=True, use_reloader=False, port=PORT)

'''
I believe y'all just need to run the following in the terminal of your cloned repository to access the virtual environment: 
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python app.py 
'''