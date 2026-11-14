"""
EVALUATION RELATED FUNCTIONS.
"""

def getUniqueEvalList(evalResponse: list[dict]) -> list[dict]:

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
        
        
