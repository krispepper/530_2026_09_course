"""
Test functions related to evaluations.
"""

import datetime

from app import app
import pandas as pd

from database import (
    getDB,
    createEvaluation,
    getEvalByClass,
    getEvalListDeptChair,
    getEvalListInstructor,
    getEvalListStudent,
    getEvalQuestions,
    getEvalResponses,
    getEvalStatus,
    getSpecEval, 
    saveEvalResponse, 
    saveEvalStatus, 
    isEvaluationPastDue, 
)
from evaluation import getAvgCourseRating, getUniqueEvalList, organizeEval


class Test_getEvalListStudent:
    """
    Tests for function getEvalListStudent.

    written by Carrie.
    """
    # variables for mutliple tests
    # IDs for userID (DB ID)
    testStudentID = "STU001"
    testNonexistentD = "DNE000"
    testStudentIDNone = "STU002"
    testEmptyID = ""

    expectedKeys = [
        "studentID",
        "evalID",
        "courseID",
        "secID",
        "term",
        "enrollID",
        "deadline",
        "status",
        "displayStatus"
    ]

    def test_studentEval(self):
        """Check that function returns evaluation responses for a specific student."""
        # get keys from first returned dict
        keys = [key for key in getEvalListStudent(self.testStudentID)[0]]
        assert keys == self.expectedKeys

    def test_studentNoEval(self):
            """Check that function returns error message for user with no evaluations."""
            assert getEvalListStudent(self.testStudentIDNone) == "No evaluation responses found."

    def test_NonexistentEval(self):
        """Check that function returns error message for a nonesistant ID."""
        assert getEvalListStudent(self.testNonexistentD) == "No evaluation responses found."

    def test_EmptyEval(self):
        """Check that function returns error message for empty string ID."""
        assert getEvalListStudent(self.testEmptyID) == "No evaluation responses found."

class Test_getEvalListInstructor:
    """
    Tests for function getEvalListInstructor.

    written by Carrie.
    """
    # variables for mutliple tests
    # IDs for userID (DB ID)
    testInstructorID = "INS001"
    testNonexistentD = "DNE000"
    testInstructorIDNone = "INS002"
    testEmptyID = ""

    expectedKeys = [
        "evalResponseID",
        "studentID",
        "response",
        "created_at",
        "last_modified",
        "enrollID",
        "fieldID",
        "evalID"
    ]

    def test_instructorEval(self):
        """Check that function returns evaluation responses for a specific instructor."""
        # get keys from first returned dict
        keys = [key for key in getEvalListInstructor(self.testInstructorID)[0]]
        assert keys == self.expectedKeys

    def test_instructorNoEval(self):
        """Check that function returns error message for user with no evaluations."""
        assert getEvalListInstructor(self.testInstructorIDNone) == "No evaluation responses found."

    def test_NonexistentEval(self):
        """Check that function returns error message for a nonesistant ID."""
        assert getEvalListInstructor(self.testNonexistentD) == "No evaluation responses found."

    def test_EmptyEval(self):
        """Check that function returns error message for empty string ID."""
        assert getEvalListInstructor(self.testEmptyID) == "No evaluation responses found."

class Test_getEvalListDeptChair:
    """
    Tests for function getEvalListDeptChair.

    written by Carrie.
    """
    # variables for mutliple tests
    # IDs for userID (DB ID)
    testDeptChairID = "DEP001"
    testNonexistentD = "DNE000"
    testDeptChairIDNone = "DEP002"
    testEmptyID = ""

    expectedKeys = [
        "evalResponseID",
        "studentID",
        "response",
        "created_at",
        "last_modified",
        "enrollID",
        "fieldID",
        "evalID"
    ]

    def test_deptChairEval(self):
        """Check that function returns evaluation responses for a specific dept Chair."""
        # get keys from first returned dict
        keys = [key for key in getEvalListDeptChair(self.testDeptChairID)[0]]
        assert keys == self.expectedKeys

    def test_instructorNoEval(self):
        """Check that function returns error message for user with no evaluations."""
        assert getEvalListDeptChair(self.testDeptChairIDNone) == "No evaluation responses found."

    def test_NonexistentEval(self):
        """Check that function returns error message for a nonesistant ID."""
        assert getEvalListDeptChair(self.testNonexistentD) == "No evaluation responses found."

    def test_EmptyEval(self):
        """Check that function returns error message for empty string ID."""
        assert getEvalListDeptChair(self.testEmptyID) == "No evaluation responses found."


class Test_getSpecEval:
    """
    Tests for function getSpecEval.
    
    written by Carrie.
    """
    # variables for mutliple tests
    # IDs for userID (DB ID)
    testEvalID = "CSC-530-050-f26"
    testStudentID = "STU001"
    testStudentIDNone = "STU002"
    testNonexistentD = "DNE000"
    testEmptyID = ""

    expectedKeys = [
        "fieldID",
        "title",
        "response",
        "created_at",
        "last_modified"
    ]

    def test_studentEval(self):
        """Check that function returns evaluation responses for a specific student."""
        # get keys from first returned dict
        keys = [key for key in getSpecEval(self.testEvalID, self.testStudentID)[0]]
        print (keys)
        assert keys == self.expectedKeys

    # This test won't work anymore because we are not returning nothing, we are returning the 
    # questions even if they were not completed. I made a new test for this! 
    # def test_studentNoEval(self):
    #     """Check that function returns evaluation responses for a specific student."""
    #     assert getSpecEval(self.testEvalID, self.testStudentIDNone) == "No evaluation responses found."

    def test_NonexistentEval(self):
        """Check that function returns error message for a nonesistant ID."""
        assert getEvalListDeptChair(self.testNonexistentD) == "No evaluation responses found."

    def test_EmptyEval(self):
        """Check that function returns error message for empty string ID."""
        assert getEvalListDeptChair(self.testEmptyID) == "No evaluation responses found."


class Test_getUniqueEvalList:
    """
    Tests for function getUniqueEvalList.

    written by Carrie.
    """
    # variables for mutliple tests
    TestEvalReponse = [
        {
            'evalResponseID': 1, 
            'studentID': 'STU001', 
            'response': '9.8', 
            'created_at': datetime.datetime(2026, 11, 12, 22, 46, 23), 
            'last_modified': datetime.datetime(2026, 11, 12, 22, 46, 23), 
            'enrollID': 1,
            'fieldID': 1, 
            'evalID': 'CSC-530-050-f26'
        }, 
        {
            'evalResponseID': 2, 
            'studentID': 'STU001', 
            'response': 'everything', 
            'created_at': datetime.datetime(2026, 11, 12, 22, 48, 2), 
            'last_modified': datetime.datetime(2026, 11, 30, 22, 47, 38), 
            'enrollID': 1, 
            'fieldID': 2, 
            'evalID': 'CSC-530-050-f26'
        }
    ]
    testUniqueEvals = [{'studentID': 'STU001', 'enrollID': 1, 'evalID': 'CSC-530-050-f26'}]
    testEmptyEval = [{}]


    def test_studentEval(self):
        """Check that function returns evaluation responses for a specific student."""
        assert getUniqueEvalList(self.TestEvalReponse) == self.testUniqueEvals

    def test_studentNoEval(self):
        """Check that function returns error message for empty eval."""
        assert getUniqueEvalList(self.testEmptyEval) == "No evaluations found."

class Test_getAvgCourseRating:
    """
    Tests for function getAvgCourseRating.
    
    written by Carrie.
    """
    evalResponses = [
    {'evalResponseID': '5', 'studentID': 'STU003', 'response': '0.9', 'created_at': '2026-11-12 22:46:23', 'last_modified': '2026-11-12 22:46:23', 'enrollID': '3', 'fieldID': '1', 'evalID': 'CSC-530-050-f26', 'title': 'Rate this course out of 10', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'}, 
    {'evalResponseID': '6', 'studentID': 'STU003', 'response': 'nothing', 'created_at': '2026-11-12 22:48:02', 'last_modified': '2026-11-21 22:47:38', 'enrollID': '3', 'fieldID': '2', 'evalID': 'CSC-530-050-f26', 'title': 'What did you like about this course?', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'},
    {'evalResponseID': '3', 'studentID': 'STU002', 'response': '5.1', 'created_at': '2026-10-12 22:46:23', 'last_modified': '2026-11-12 22:46:23', 'enrollID': '2', 'fieldID': '1', 'evalID': 'CSC-530-050-f26', 'title': 'Rate this course out of 10', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'}, 
    {'evalResponseID': '4', 'studentID': 'STU002', 'response': 'something', 'created_at': '2026-10-12 22:48:02', 'last_modified': '2026-11-30 22:47:38', 'enrollID': '2', 'fieldID': '2', 'evalID': 'CSC-530-050-f26', 'title': 'What did you like about this course?', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'},
    {'evalResponseID': '1', 'studentID': 'STU001', 'response': '9.8', 'created_at': '2026-11-12 22:46:23', 'last_modified': '2026-11-12 22:46:23', 'enrollID': '1', 'fieldID': '1', 'evalID': 'CSC-530-050-f26', 'title': 'Rate this course out of 10', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'}, 
    {'evalResponseID': '2', 'studentID': 'STU001', 'response': 'everything', 'created_at': '2026-11-12 22:48:02', 'last_modified': '2026-11-21 22:47:38', 'enrollID': '1', 'fieldID': '2', 'evalID': 'CSC-530-050-f26', 'title': 'What did you like about this course?', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'}
    ]

    evalResponses2 = [
    {'evalResponseID': '1', 'studentID': 'STU003', 'response': '0.9', 'created_at': '2026-11-12 22:46:23', 'last_modified': '2026-11-12 22:46:23', 'enrollID': '3', 'fieldID': '1', 'evalID': 'CSC-530-050-f26', 'title': 'Rate this course out of 10', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'}, 
    {'evalResponseID': '2', 'studentID': 'STU003', 'response': '2.1', 'created_at': '2026-11-12 22:48:02', 'last_modified': '2026-11-21 22:47:38', 'enrollID': '3', 'fieldID': '2', 'evalID': 'CSC-530-050-f26', 'title': 'Rate this course out of 10', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'},
    {'evalResponseID': '3', 'studentID': 'STU002', 'response': '5.1', 'created_at': '2026-10-12 22:46:23', 'last_modified': '2026-11-12 22:46:23', 'enrollID': '2', 'fieldID': '1', 'evalID': 'CSC-530-050-f26', 'title': 'Rate this course out of 10', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'}, 
    {'evalResponseID': '4', 'studentID': 'STU002', 'response': '9.0', 'created_at': '2026-10-12 22:48:02', 'last_modified': '2026-11-30 22:47:38', 'enrollID': '2', 'fieldID': '2', 'evalID': 'CSC-530-050-f26', 'title': 'Rate this course out of 10', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'},
   ]
    rating_col = "Rate this course out of 10"
    bad_rating_col = "course rating"

    def test_ratingColExists(self):
        """Check a course average is returned when the given column is found."""
        assert getAvgCourseRating(self.evalResponses, self.rating_col) == 5.27

    def test_ratingColNotExists(self):
        """Check a error msg is returned when the given column is not found."""
        assert getAvgCourseRating(self.evalResponses, self.bad_rating_col) == 'There are 0 evaluation fields named "course rating."'

    def test_ratingColExistsMultiple(self):
        """Check a error msg is returned when the given column is found multiple times."""
        assert getAvgCourseRating(self.evalResponses2, self.rating_col) == 'There are 2 evaluation fields named "Rate this course out of 10."'

class Test_organizeEval:
    """
    Tests for function organizeEval.
    
    written by Carrie.
    """
    evalResponses = [
    {'evalResponseID': '5', 'studentID': 'STU003', 'response': '0.9', 'created_at': '2026-11-12 22:46:23', 'last_modified': '2026-11-12 22:46:23', 'enrollID': '3', 'fieldID': '1', 'evalID': 'CSC-530-050-f26', 'title': 'Rate this course out of 10', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'}, 
    {'evalResponseID': '6', 'studentID': 'STU003', 'response': 'nothing', 'created_at': '2026-11-12 22:48:02', 'last_modified': '2026-11-21 22:47:38', 'enrollID': '3', 'fieldID': '2', 'evalID': 'CSC-530-050-f26', 'title': 'What did you like about this course?', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'},
    {'evalResponseID': '3', 'studentID': 'STU002', 'response': '5.1', 'created_at': '2026-10-12 22:46:23', 'last_modified': '2026-11-12 22:46:23', 'enrollID': '2', 'fieldID': '1', 'evalID': 'CSC-530-050-f26', 'title': 'Rate this course out of 10', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'}, 
    {'evalResponseID': '4', 'studentID': 'STU002', 'response': 'something', 'created_at': '2026-10-12 22:48:02', 'last_modified': '2026-11-30 22:47:38', 'enrollID': '2', 'fieldID': '2', 'evalID': 'CSC-530-050-f26', 'title': 'What did you like about this course?', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'},
    {'evalResponseID': '1', 'studentID': 'STU001', 'response': '9.8', 'created_at': '2026-11-12 22:46:23', 'last_modified': '2026-11-12 22:46:23', 'enrollID': '1', 'fieldID': '1', 'evalID': 'CSC-530-050-f26', 'title': 'Rate this course out of 10', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'}, 
    {'evalResponseID': '2', 'studentID': 'STU001', 'response': 'everything', 'created_at': '2026-11-12 22:48:02', 'last_modified': '2026-11-21 22:47:38', 'enrollID': '1', 'fieldID': '2', 'evalID': 'CSC-530-050-f26', 'title': 'What did you like about this course?', 'fieldSubject': 'misc', 'courseID': '530', 'secID': '50', 'term': 'F26'}
    ]

    orgEvalDict = {
        'studentID': {0: 'STU001', 1: 'STU002', 2: 'STU003'},
        'Rate this course out of 10': {0: '9.8', 1: '5.1', 2: '0.9'},
        'What did you like about this course?': {0: 'everything',
        1: 'something',
        2: 'nothing'},
        'Initial Submission': {0: '2026-11-12 22:46:23',
        1: '2026-10-12 22:46:23',
        2: '2026-11-12 22:46:23'},
        'last Modified': {0: '2026-11-21 22:47:38',
        1: '2026-11-30 22:47:38',
        2: '2026-11-21 22:47:38'}
    }


    def test_organizeEval(self):
        """Check evaluations are reformatted with one row per student."""
        organized_df= organizeEval(self.evalResponses)
        # test values are correct (comparing df is not as reliable)
        assert organized_df.to_dict() == self.orgEvalDict
        # test returns pandas dataframe 
        assert isinstance(organized_df, pd.DataFrame)

    
class Test_getEvalByClass:
    """
    Tests for function getEvalByClass.

    written by Carrie.
    """
    # variables for test
    testCourseID = 530
    testSecID = 50
    testTerm = 'F26'

    expectedKeys = [
        'evalResponseID',
        'studentID', 
        'response', 
        'created_at', 
        'last_modified', 
        'enrollID', 
        'fieldID', 
        'evalID', 
        'title', 
        'fieldSubject', 
        'courseID', 
        'secID', 
        'term'
    ]


    def test_evalsExist(self):
        """Check function returns evaluations of a given course."""
        # get keys from returned evalResponses
        keys = [key for key in getEvalByClass(self.testCourseID, 
            self.testSecID, 
            self.testTerm)[0]]
        # check keys are the same
        assert keys == self.expectedKeys


class Test_EvaluationFeatures: 
    """Tests for new evaluation features. - Faith"""

    testStudentID = "STU002"
    testEnrollID = "428"
    testEvalID = "CSC-530-050-F26"

    def test_standardQuestions(self): 
        """Check that all 10 standard questions were created with a new evaluation."""
        # This will fail until we remove prior made evaluations from the database. 

        questions = getEvalQuestions(self.testEvalID)

        assert len(questions) == 10

    def test_standardQuestionsNoResponse(self):
        """Check that standard questions still appear even when a student has not answered them."""
        # This will fail until we remove prior made evaluations from the database. 

        questions = getSpecEval(self.testEvalID, self.testStudentID)

        assert len(questions) == 10

    def test_standardQuestionNone(self): 
        """Check that questions with no response (unanswered fields) have 'None' values."""

        questions = getSpecEval(self.testEvalID, self.testStudentID)

        assert all(question["response"] is None for question in questions)
    
    # def test_savedProgressPartial(self):
    #     """Check that students are able to save progress when the evaluation is only partially completed."""

    #     saveEvalResponse(self.testStudentID, self.testEnrollID, self.testEvalID, 1, "8")
    #     responses = getEvalResponses(self.testEnrollID, self.testEvalID)

    #     assert len(responses) > 0

    # def test_savedProgressStay(self):
    #     """Check that when students re-open a saved evaluation, their work is still saved."""

    #     responses = getEvalResponses(self.testEnrollID, self.testEvalID)

    #     assert responses[0]["response"] == "8"

    # def test_evaluationStatus(self):
    #     """Check that saving an evaluation saves status."""

    #     saveEvalStatus(self.testEnrollID, self.testEvalID, "In Progress")
    #     status = getEvalStatus(self.testEnrollID, self.testEvalID)

    #     assert status == "In Progress"

    def test_deadline(self):
        """Check that past due evaluations cannot be saved or submitted."""

        pastDue = isEvaluationPastDue(self.testEvalID)

        assert pastDue == True

    # def test_blockDuplicate(self):
    #     """Check that only one evaluation can be made (making a second one is blocked)"""
        
    #     result = createEvaluation(
    #         self.testEvalID,
    #         "DEP001",
    #         "428",
    #         "PHY",
    #         "S27",
    #         "Test Evaluation",
    #         None
    #     )

    #     assert result != self.testEvalID

        