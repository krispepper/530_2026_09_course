import os
import re 

from dotenv import load_dotenv
from flask import Flask, request, jsonify

from database import getDB, createUser, edit_evaluationQuestion

app = Flask(__name__) 

load_dotenv()

PORT = os.getenv("PORT")

@app.route("/")
def index():
    return "route options:/home /student /instructor /admin /database-check"

@app.route("/homepage")
def home(): 
    return "Wooo it's running!"

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

'''
I believe y'all just need to run the following in the terminal of your cloned repository to access the virtual environment: 
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python app.py 
'''

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

if __name__ == "__main__": 
    app.run(debug=True, use_reloader=False, port=PORT)


@app.route("/evaluations/<eval_ID>/questions/<int:field_ID>", methods=["PUT"])
def edit_question(eval_ID, field_ID):
    data = request.get_json()

    if not data: 
        return jsonify({"error":"Missing request data"}), 400 

    title = data.get("title")
    fieldType = data.get("fieldType")
    fieldSubject = data.get("fieldSubject")
    options = data.get("options")

    if not all([title, fieldType, fieldSubject]):
        return jsonify({"error": "Title, field type, and field subject are required."}), 400

    result = edit_evaluationQuestion(eval_ID, field_ID, title, fieldType, fieldSubject, options)

    if result == 1: 
        return jsonify({"message": "Question was sucessfully updated"}), 200 

    return jsonify({"message":"No rows were changed. Check if question exists or the change was identical to the original."}), 200
