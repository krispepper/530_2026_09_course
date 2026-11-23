# Course Evaluation 
***
Members: 
Carrie Smithing, Faith Mock, Hugo Ledesma, Ryan Maselli
***
## Clone GitHub
* Navigate to directory you want to clone GitHub repository into 
* Run the below command in terminal
```bash
git clone https://github.com/krispepper/530_2026_09_course.git
```

## Set up venv
* Navigate to the repository folder made in Clone GitHub step
* run the following command in the terminal 
```bash
python -m venv .venv
```
## Activate venv with one of the following:
1. macOS/Linux:
```bash
source .venv/bin/activate
```
2. Windows bash:
```bash
.venv/Scripts/activate
```
3. Windows Command Prompt:
```bash
 .venv/Scripts/activate.bat
```
4. Windows Powershell:
```bash
.venv/Scripts/Activate.ps1
```
* When active your terminal should display "(venv)" in front of your current woeking directory (CWD)

## Install requirements
* if not done already, activate venv
* in the terminal run 
```bash
pip install -r requirements.txt
```

* If you want to reinstall or uninstall packages, just delete the .venv folder and redo set up venv followed by install requirements

## Set up .env file
* Make a copy of [.env.example](.env.example)
* Edit the variable values as the comments in file say to

## Running the Application
* in the terminal run 
```bash 
python app.py
```

## Running Pytest:
* cd to root folder 
```bash
 cd home/groupprojects/530_2026_09_course
 ```
 - adjust route as needed
* If not already active, activate venv
* run in command line:
```bash 
python -m pytest
```
  - to check a specific test run 
    ```bash 
    pytest path/to/test::testClass::unitTest
    ```
  - example: 
    ```bash
    pytest tests/test_eval.py::Test_getEvalListStudent::test_studentEval
    ```

## User Acceptance Testing:
* User acceptance testing information can be found in the [docs](docs) folder 
    - [Sprint 1](docs/Sprint%201%20UAT.txt)
    - [Sprint 2](docs/Sprint%202%20UAT.txt)
    - Sprint 3 - To be created
    - Sprint 4 - To be created