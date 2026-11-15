"""
EVALUATION RELATED FUNCTIONS.
"""

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
        
        
