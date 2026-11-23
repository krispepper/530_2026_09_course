# All tests were all written by Hugo.
from database import getEvaluationFormInfo, getEnrollmentId, submitEvaluation


# Tests the function getEvaluationFormInfo.
class Test_getEvaluationFormInfo:
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
        expected = [
            {'evalID': 'CSC-530-050-f26', 'title': 'Rate this course out of 10', 'fieldType': 'int', 'fieldID': 1, 'options': None, 'fieldSubject':'misc'},
            {'evalID': 'CSC-530-050-f26', 'title': 'What did you like about this course?', 'fieldType': 'shortText', 'fieldID': 2, 'options': None, 'fieldSubject':'misc'},
            {'evalID': 'CSC-530-50-F26', 'title': 'The instructor presents the subject matter in a clear and understandable way.', 'fieldType': 'int', 'fieldID': 1, 'options': '1,2,3,4,5,NA', 'fieldSubject':'instructor'},
            {'evalID': 'CSC-530-50-F26', 'title': 'The instructor uses class time effectively and efficiently.', 'fieldType': 'int', 'fieldID': 2, 'options': '1,2,3,4,5,NA', 'fieldSubject':'instructor'}, 
            {'evalID': 'CSC-530-50-F26', 'title': 'The instructor creates an atmosphere that encourages questions and discussion.', 'fieldType': 'int', 'fieldID': 3, 'options': '1,2,3,4,5,NA', 'fieldSubject':'instructor'},
            {'evalID': 'CSC-530-50-F26', 'title': 'The instructor treats students with respect.', 'fieldType': 'int', 'fieldID': 4, 'options': '1,2,3,4,5,NA', 'fieldSubject':'instructor'}, 
            {'evalID': 'CSC-530-50-F26', 'title': 'Exams and assignments are well connected to course objectives.', 'fieldType': 'int', 'fieldID': 5, 'options': '1,2,3,4,5,NA', 'fieldSubject':'course'},
            {'evalID': 'CSC-530-50-F26', 'title': 'Assigned materials are relevant to class.', 'fieldType': 'int', 'fieldID': 6, 'options': '1,2,3,4,5,NA', 'fieldSubject':'course'},
            {'evalID': 'CSC-530-50-F26', 'title': 'I would recommend this course to other students.', 'fieldType': 'int', 'fieldID': 7, 'options': '1,2,3,4,5,NA', 'fieldSubject':'course'},
            {'evalID': 'CSC-530-50-F26', 'title': 'This course has improved my critical thinking skills.', 'fieldType': 'int', 'fieldID': 8, 'options': '1,2,3,4,5,NA', 'fieldSubject':'learning'}, 
            {'evalID': 'CSC-530-50-F26', 'title': 'What did you like most about this course?', 'fieldType': 'shortText', 'fieldID': 9, 'options': None, 'fieldSubject':'misc'},
            {'evalID': 'CSC-530-50-F26', 'title': 'What suggestions do you have for improving this course?', 'fieldType': 'shortText', 'fieldID': 10, 'options': None, 'fieldSubject':'misc'},
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