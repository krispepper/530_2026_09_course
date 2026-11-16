# This file is to test adding standard evaluation questions
    # written by faith

import database

# Tests for "add_standardQuestions" from database.py
class Test_addStandardQuestions:

    # Variables for multiple tests
    testEvalID = "TEST-EVAL"

    # Check that 10 standard questions are added to an evaluation
    def test_addStandardQuestions(self):
        database.add_standardQuestions(self.testEvalID)

        db = database.getDB()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM formField WHERE evalID = %s", (self.testEvalID,) )

        questions = cursor.fetchall()

        assert len(questions) == 10

        cursor.close()
        db.close()