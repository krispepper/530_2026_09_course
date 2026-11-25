# All tests were all written by Hugo.
from database import getEnrollmentId, getEvaluationFormInfo


# Tests the function getEvaluationFormInfo.
class Test_getEvaluationFormInfo:
    validCourseId = "428"
    invalidCourseId = "999"
    emptyCourseId = ""
    validSecId = "1"
    invalidSecId = "999"
    emptySecId = ""
    validTerm = "S27"
    invalidTerm = "XYZ"
    emptyTerm = ""


    def test_AllValid(self):
        """Check that the function returns ."""
        expected = [
            {
                'evalID': 'PHY-428-001-S27', 
                'title': 'Course Rating', 
                'fieldType': 'int', 
                'fieldID': 1, 
                'options': None, 
                'fieldSubject': 'misc'
            }, 
            {
                'evalID': 'PHY-428-001-S27', 
                'title': 'Would you recommend this course?', 
                'fieldType': 'shortText', 
                'fieldID': 2, 
                'options': None, 
                'fieldSubject': 'misc'
            }
        ]
        results = getEvaluationFormInfo(self.validCourseId, self.validSecId, self.validTerm)
        assert results == expected

    def test_invalidCourseId(self):
        """Check that the function returns that the data could not be found due to an invalid course ID."""
        assert getEvaluationFormInfo(self.invalidCourseId, self.validSecId, self.validTerm) == "Data not found."

    def test_emptyCourseId(self):
        """Check that the function returns that the data could not be found due to an empty course ID."""
        assert getEvaluationFormInfo(self.emptyCourseId, self.validSecId, self.validTerm) == "Data not found."

    def test_invalidSecId(self):
        """Check that the function returns that the data could not be found due to an invalid sec ID."""
        assert getEvaluationFormInfo(self.validCourseId, self.invalidSecId, self.validTerm) == "Data not found."

    def test_emptySecId(self):
        """Check that the function returns that the data could not be found due to an empty sec ID."""
        assert getEvaluationFormInfo(self.validCourseId, self.emptySecId, self.validTerm) == "Data not found."

    def test_invalidTerm(self):
        """Check that the function returns that the data could not be found due to an invalid term."""
        assert getEvaluationFormInfo(self.validCourseId, self.validSecId, self.invalidTerm) == "Data not found."

    def test_emptyTerm(self):
        """Check that the function returns that the data could not be found due to an empty term."""
        assert getEvaluationFormInfo(self.validCourseId, self.validSecId, self.emptyTerm) == "Data not found."



# Tests the function getEnrollmentId.
class Test_getEnrollmentId:
    validStudentID = "STU001"
    invalidStudentID = "NOPE12"
    emptyStudentID = ""
    validCourseId = "530"
    invalidCourseId = "999"
    emptyCourseId = ""
    validSecId = "50"
    invalidSecId = "999"
    emptySecId = ""
    validTerm = "F26"
    invalidTerm = "XYZ"
    emptyTerm = ""


    def test_AllValid(self):
        """Check that the function returns ."""
        assert getEnrollmentId(self.validStudentID, self.validCourseId, self.validSecId, self.validTerm) == {'enrollID': 1}

    def test_invalidStudentID(self):
        """Check that the function returns that the enrollment ID was not found due to an invalid student ID."""
        assert getEnrollmentId(self.invalidStudentID, self.validCourseId, self.validSecId, self.validTerm) == "Enrollment ID not found."

    def test_emptyStudentID(self):
        """Check that the function returns that the enrollment ID was not found due to an empty student ID."""
        assert getEnrollmentId(self.emptyStudentID, self.validCourseId, self.validSecId, self.validTerm) == "Enrollment ID not found."

    def test_invalidCourseId(self):
        """Check that the function returns that the enrollment ID was not found due to an invalid course ID."""
        assert getEnrollmentId(self.validStudentID, self.invalidCourseId, self.validSecId, self.validTerm) == "Enrollment ID not found."

    def test_emptyCourseId(self):
        """Check that the function returns that the enrollment ID was not found due to an empty course ID."""
        assert getEnrollmentId(self.validStudentID, self.emptyCourseId, self.validSecId, self.validTerm) == "Enrollment ID not found."

    def test_invalidSecId(self):
        """Check that the function returns that the enrollment ID was not found due to an invalid sec ID."""
        assert getEnrollmentId(self.validStudentID, self.validCourseId, self.invalidSecId, self.validTerm) == "Enrollment ID not found."

    def test_emptySecId(self):
        """Check that the function returns that the enrollment ID was not found due to an empty sec ID."""
        assert getEnrollmentId(self.validStudentID, self.validCourseId, self.emptySecId, self.validTerm) == "Enrollment ID not found."

    def test_invalidTerm(self):
        """Check that the function returns that the enrollment ID was not found due to an invalid term."""
        assert getEnrollmentId(self.validStudentID, self.validCourseId, self.validSecId, self.invalidTerm) == "Enrollment ID not found."

    def test_emptyTerm(self):
        """Check that the function returns that the enrollment ID was not found due to an empty term."""
        assert getEnrollmentId(self.validStudentID, self.validCourseId, self.validSecId, self.emptyTerm) == "Enrollment ID not found."