import os

from dotenv import load_dotenv
from flask import Flask 

from database import getDB

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

if __name__ == "__main__": 
    app.run(debug=True, use_reloader=False, port=PORT)

'''
I believe y'all just need to run the following in the terminal of your cloned repository to access the virtual environment: 
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python app.py 
'''