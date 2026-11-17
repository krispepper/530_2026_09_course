"""
EVALUATION RELATED FUNCTIONS.
"""
import pandas as pd

def getUniqueEvalList(evalResponse: list[dict]) -> list[dict] | str:
    """ 
    Function returns only unique evaluations based on a list of evalResponses.
    
    attrs: 
        evalResponse (list[dict]): list of dictionaries with eval responses
    return: 
        uniqueEvals (list[dict]): returns list of dictionary containing unique evaluations
    """
    if all(eval == {} for eval in evalResponse):
        return "No evaluations found."
    
    uniqueEvals = list({
        (eval['studentID'], eval['enrollID'], eval['evalID']): {
            'studentID': eval['studentID'],
            'enrollID': eval['enrollID'],
            'evalID': eval['evalID']
        }
        for eval in evalResponse
    }.values())

    return uniqueEvals

def getAvgCourseRating(evalResponses: list[dict], rating_title: str) -> float | str:
    """ 
    Function returns average course rating based on a list of evalResponses if course rating is included.
    
    attrs: 
        evalResponses (list[dict]): list of dictionaries with eval responses
        rating_title (str): name for form field being used for course rating
    return: 
        RatingAvg (decimal): average rating of the evaluation responses
    """
    # turn eval response into data frame
    evals_df = pd.DataFrame(evalResponses)

    # subset df to only rows where title is the expected rating col
    rating_df = evals_df[evals_df["title"].str.lower() == rating_title.lower()]
    # check that all the field IDs are the same
    num_fields = rating_df["fieldID"].nunique()

    # check how many field IDs where found
    if num_fields == 1:
        # return rounded avg (##.##)
        return round(pd.to_numeric(rating_df['response']).mean(), 2)
    else:
        # if less than or more than 1 were found
        # return error msg with how many fields were found
        return f'There are {num_fields} evaluation fields named "{rating_title}."'

def organizeEval(evalResponse: list[dict]) -> pd.DataFrame:
    """ 
    Function returns evaluations responses condensed into one line per evaluation.
    
    attrs: 
        evalResponses (list[dict]): list of dictionaries with eval responses
            - right now can only process evalResponses returned by getEvalByClass 
    return: 
        evaluations (pd.DataFrame): average rating of the evaluation responses
    """
    
    df = pd.DataFrame(evalResponse)

    # get each question as a column
    evaluations = df.pivot(
        index='studentID',
        columns='title',
        values='response'
    ).reset_index()

    # removes "title" from being columns name
    evaluations.columns.name = None

    # sort by student IDs
    evaluations.sort_values(by="studentID")

    # create empty dict
    evalDates = {}

    # get the created and last modified dates for each students eval
    for evalSubmitted in getUniqueEvalList(evalResponse):
        eval_df = df[
            (df["studentID"] == evalSubmitted["studentID"]) &
            (df["enrollID"] == evalSubmitted["enrollID"]) &
            (df["evalID"] == evalSubmitted["evalID"])
            ]

        evalDates[evalSubmitted["studentID"]] = {
        "created_at": eval_df["created_at"].iloc[0],
        "last_mod": eval_df["last_modified"].max()
        }

    # sort evalDates so it will have same order as evaluations df
    sorted_evalDates= dict(sorted(evalDates.items()))

    # add dates to evaluations df
    evaluations["Initial Submission"] = [e["created_at"] for e in sorted_evalDates.values()]
    evaluations["last Modified"] = [e["last_mod"] for e in sorted_evalDates.values()]

    return evaluations