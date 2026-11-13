import datetime
import pytest

from database import getEvalListStudent, getEvalListInstructor, getEvalListDeptChair, getSpecEval
from evaluation import getUniqueEvalList

class Test_getEvalListStudent:
    """Tests for function getEvalListStudent."""
    # variables for mutliple tests
    # IDs for userID (DB ID)
    testStudentID = "STU001"
    testNonexistantD = "DNE000"
    testStudentIDNone = "STU002"
    testEmptyID = ""

    Eval = [
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

    def test_studentEval(self):
        """Check that function returns evaluation responses for a specific student."""
        assert getEvalListStudent(self.testStudentID) == self.Eval

    def test_studentNoEval(self):
            """Check that function returns error message for user with no evaluations."""
            assert getEvalListStudent(self.testStudentIDNone) == "No evaluation responses found."

    def test_nonexistantEval(self):
        """Check that function returns error message for a nonesistant ID."""
        assert getEvalListStudent(self.testNonexistantD) == "No evaluation responses found."

    def test_EmptyEval(self):
        """Check that function returns error message for empty string ID."""
        assert getEvalListStudent(self.testEmptyID) == "No evaluation responses found."


class Test_getEvalListInstructor:
    """Tests for function getEvalListInstructor."""
    # variables for mutliple tests
    # IDs for userID (DB ID)
    testInstructorID = "INS001"
    testNonexistantD = "DNE000"
    testInstructorIDNone = "INS002"
    testEmptyID = ""

    Eval = [
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

    def test_instructorEval(self):
        """Check that function returns evaluation responses for a specific instructor."""
        assert getEvalListInstructor(self.testInstructorID) == self.Eval

    def test_instructorNoEval(self):
        """Check that function returns error message for user with no evaluations."""
        assert getEvalListInstructor(self.testInstructorIDNone) == "No evaluation responses found."

    def test_nonexistantEval(self):
        """Check that function returns error message for a nonesistant ID."""
        assert getEvalListInstructor(self.testNonexistantD) == "No evaluation responses found."

    def test_EmptyEval(self):
        """Check that function returns error message for empty string ID."""
        assert getEvalListInstructor(self.testEmptyID) == "No evaluation responses found."

class Test_getEvalListDeptChair:
    """Tests for function getEvalListDeptChair."""
    # variables for mutliple tests
    # IDs for userID (DB ID)
    testDeptChairID = "DEP001"
    testNonexistantD = "DNE000"
    testDeptChairIDNone = "DEP002"
    testEmptyID = ""

    Eval = [
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

    def test_deptChairEval(self):
        """Check that function returns evaluation responses for a specific dept Chair."""
        assert getEvalListDeptChair(self.testDeptChairID) == self.Eval

    def test_instructorNoEval(self):
        """Check that function returns error message for user with no evaluations."""
        assert getEvalListDeptChair(self.testDeptChairIDNone) == "No evaluation responses found."

    def test_nonexistantEval(self):
        """Check that function returns error message for a nonesistant ID."""
        assert getEvalListDeptChair(self.testNonexistantD) == "No evaluation responses found."

    def test_EmptyEval(self):
        """Check that function returns error message for empty string ID."""
        assert getEvalListDeptChair(self.testEmptyID) == "No evaluation responses found."


class Test_getSpecEval:
    """Tests for function getSpecEval."""
    # variables for mutliple tests
    # IDs for userID (DB ID)
    testEvalID = "CSC-530-050-f26"
    testStudentID = "STU001"
    testStudentIDNone = "STU002"
    testNonexistantD = "DNE000"
    testEmptyID = ""

    fields = [
        {
            'fieldID': 1, 
            'title': 'Rate this course out of 10', 
            'response': '9.8', 
            'created_at': datetime.datetime(2026, 11, 12, 22, 46, 23), 
            'last_modified': datetime.datetime(2026, 11, 12, 22, 46, 23)
        }, 
        {
            'fieldID': 2, 
            'title': 'What did you like about this course?', 
            'response': 'everything', 
            'created_at': datetime.datetime(2026, 11, 12, 22, 48, 2), 
            'last_modified': datetime.datetime(2026, 11, 30, 22, 47, 38)
        }
    ]

    def test_studentEval(self):
        """Check that function returns evaluation responses for a specific student."""
        assert getSpecEval(self.testEvalID, self.testStudentID) == self.fields

    def test_studentNoEval(self):
        """Check that function returns evaluation responses for a specific student."""
        assert getSpecEval(self.testEvalID, self.testStudentIDNone) == "No evaluation responses found."

    def test_nonexistantEval(self):
        """Check that function returns error message for a nonesistant ID."""
        assert getEvalListDeptChair(self.testNonexistantD) == "No evaluation responses found."

    def test_EmptyEval(self):
        """Check that function returns error message for empty string ID."""
        assert getEvalListDeptChair(self.testEmptyID) == "No evaluation responses found."


class Test_getUniqueEvalList:
    """Tests for function getUniqueEvalList."""
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
        