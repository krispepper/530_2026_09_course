from flask import Flask 

app = Flask(__name__) 

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

if __name__ == "__main__": 
    app.run(debug=True, use_reloader=False)

'''
I believe y'all just need to run the following in the terminal of your cloned repository to access the virtual environment: 
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python app.py 
'''