"""
EXPORT RELATED FUNCTIONS.
"""
from datetime import datetime
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd

from database import (
    getCourseDept,
    getCourseName,
    getEvalByClass,
    getInstructorByCourse,
    getRoleID,
    getRoster,
    getUserNameFromId,
)
from evaluation import getAvgCourseRating, getUniqueEvalList, organizeEval


def getTimestamp():
    return datetime.now().strftime('%Y.%m.%d_%H.%M.%S')

def getCourseInfoDict (courseID, secID, term) -> dict:
    ### get info for export: ###
    
    # eval responses for class
    evalResponses = getEvalByClass(courseID, secID, term)

    # instructor role ID
    userID = getInstructorByCourse(courseID, secID, term)
    insID = getRoleID(userID)

    # instructor name
    name = getUserNameFromId(userID)

    # course name 
    courseName = getCourseName(courseID)

    # number of students
    numStu = len(getRoster(courseID=courseID, secID=secID, term=term))

    # total number of evals submitted
    totSub = len(getUniqueEvalList(evalResponses))

    # percent of evals submitted 
    # assuming student are only allowed 1 eval (will update later with limit story)
    limit = 1 # getEvalLimit(courseID, secID, termID)
    perSub = (totSub/(numStu*limit))*100 
    
    # department
    dept = getCourseDept(courseID)

    # most recent eval submission 

    lastEval=max([response["last_modified"] for response in evalResponses if response["last_modified"] is not None])

    # course rating 
    courseRatingAvg = getAvgCourseRating(evalResponses, "Course Rating")
    if isinstance(courseRatingAvg, str):
        courseRating = "N/A"
    else:
        courseRating = courseRatingAvg

    gen_data = {
        "Instructor Name": f"{name["firstName"]} {name["lastName"]}",
        "Instructor ID": insID,
        "Course Name": courseName,
        "Department": dept,
        "Course ID": courseID,
        "Section ID": secID,
        "Term": term,
        "Number of Students": numStu,
        "Percentage of Evaluations Submitted": perSub,
        "Timestamp of last evaluation submission": lastEval,
        "Course Rating": courseRating
    }

    return gen_data

def exportCSVCourse(courseID: int, secID: int, term: str) -> str:

    # get general course info 
    gen_data = getCourseInfoDict(courseID, secID, term)
    
    # eval responses for class
    evalResponses = getEvalByClass(courseID, secID, term)

    # filenames
    InstructorID = getInstructorByCourse(courseID, secID, term)
    genFile = f"{InstructorID}_{courseID}_{secID}_general_{getTimestamp()}.csv"
    evalsFile = f"{InstructorID}_{courseID}_{secID}_feedback_{getTimestamp()}.csv"

    # create ZIP file in memory
    zip_output = BytesIO()

    with ZipFile(zip_output, 'w', ZIP_DEFLATED) as zip_file:

        o1 = BytesIO()

        # general evaluation information file
        gen_df = pd.DataFrame([gen_data])
        gen_df.to_csv(o1, index=False)

        zip_file.writestr(
            genFile,
            o1.getvalue()
        )

        o2 = BytesIO()

        # export evaluations information
        organizeEval(evalResponses).to_csv(o2, index=False)

        zip_file.writestr(
            evalsFile,
            o2.getvalue()
        )

    # resest memory buffer position
    zip_output.seek(0)

    InstructorID = getInstructorByCourse(courseID, secID, term)
    zipFileName = f"{InstructorID}_{courseID}_{secID}_course_exports_{getTimestamp()}.zip"

    return zip_output, zipFileName

def exportXlsxCourse(courseID: int, secID: int, term: str):
        
    # get general course info 
    gen_data = [getCourseInfoDict(courseID, secID, term)]
    gen_df = pd.DataFrame(gen_data)
    
    # eval responses for class
    evalResponses = getEvalByClass(courseID, secID, term)
    eval_df = organizeEval(evalResponses)

    # export xlsx file
    dfs_export = {"general stats": gen_df, "feedback": eval_df}

    InstructorID = getInstructorByCourse(courseID, secID, term)
    filename = f"{InstructorID}_{courseID}_{secID}_feedback_{getTimestamp()}.xlsx"

    # create file in memory
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for name, df in dfs_export.items():
            df.to_excel(writer, sheet_name=name, index=False)

    output.seek(0)

    return output, filename