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


        
