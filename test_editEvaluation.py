# This file is to test editing evaluation questions 
    # written by faith 

import database
from database import edit_evaluationQuestion

# Tests for "edit_evaluationQuestion" from database.py 
class Test_edit_evaluationQuestion:

    # Variables for multiple tests
    testEvalID = "TEST-EVAL"
    testFieldID = 1
    testNonexistentEval = "DNE-EVAL"
    testNonexistentField = 444

    # Check that an existing evaluation question can be updated 
    def test_editExistingQuestion(self):
        result = edit_evaluationQuestion(self.testEvalID,self.testFieldID,
            "Updated question?","shortText","course",None)
        assert result == 1

    # Check that a nonexistent evaluation question is not updated.
    def test_editNonexistentQuestion(self):
        result = edit_evaluationQuestion(self.testNonexistentEval,self.testNonexistentField,
            "Updated question?","shortText","course",None)
        assert result == 0

    # Check that the updated question values were saved
    def test_updatedQuestionValues(self):
        edit_evaluationQuestion(self.testEvalID,self.testFieldID,
            "Updated question?","shortText","course",None)

        db = database.getDB()
        cursor = db.cursor()

        cursor.execute(
            """SELECT title, fieldType, fieldSubject, options FROM formField WHERE evalID = %s AND fieldID = %s""",
            (self.testEvalID, self.testFieldID)
        )

        question = cursor.fetchone()
        assert question == ("Updated question?", "shortText", "course", None)

        cursor.close()
        db.close()

# Check that editing a question does not delete student responses
    def test_preserveStudentResponses(self):
        db = database.getDB()
        cursor = db.cursor()

        cursor.execute("""SELECT * FROM evalResponse WHERE evalID = %s AND fieldID = %s""",
            (self.testEvalID, self.testFieldID)
        )

        responsesBefore = cursor.fetchall()
        assert len(responsesBefore) > 0 # make sure there are responses to compare 

        cursor.close()
        db.close()

        edit_evaluationQuestion(self.testEvalID,self.testFieldID,
            "Another updated question?","shortText","course",None)

        db = database.getDB()
        cursor = db.cursor()

        cursor.execute("""SELECT * FROM evalResponse WHERE evalID = %s AND fieldID = %s""",
            (self.testEvalID, self.testFieldID)
        )

        responsesAfter = cursor.fetchall()
        assert responsesBefore == responsesAfter

        cursor.close()
        db.close()