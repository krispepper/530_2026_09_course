"""
Test functions related to courses.
"""

from database import (
    getCourseDept, 
    getCourseListStudent, 
    getCourseListInstructor, 
    getCourseListDeptChair,
    getCourseName
)

class Test_getCourseDept:
    """
    Tests for function getCourseDept.

    written by Carrie.
    """
    # variables for tests
    testCourseID = 530
    testNonexistentCourseID = 0
    expectedCourse = "CSC"

    def test_courseExists(self):
        """Checks correct course dept is returned for a given course."""
        assert getCourseDept (self.testCourseID) == self.expectedCourse

    def test_courseNotExists(self):
        """Checks error message is returned for a given course that does not exist."""
        assert getCourseDept(self.testNonexistentCourseID) == f"No dept id for course {self.testNonexistentCourseID}."

class Test_getCourseListStudent:
    """
    Tests for function getCourseListStudent.

    written by Carrie.
    """
    # variables for tests
    testStudentID = "STU001"
    testNonexistentStudentID = "STU002"
    testStudentName = "Test Student2"
    expectedKeys = [
        "name",
        "courseID",
        "secID",
        "term"
    ]

    def test_courseListStudent(self):
        """Checks function returns course list of a given student."""
        # get keys from returned evalResponses
        keys = [key for key in getCourseListStudent(self.testStudentID)[0].keys()]
        # check keys are the same
        assert keys == self.expectedKeys

    def test_courseListStudentNoEvals(self):
        """Checks function returns error message for given student with no evaluations."""
        print(getCourseListStudent(self.testNonexistentStudentID))
        # check keys are the same
        assert getCourseListStudent(self.testNonexistentStudentID) == f"No courses found for {self.testStudentName}."

class Test_getCourseListInstructor:
    """
    Tests for function getCourseListInstructor.

    written by Carrie.
    """
    # variables for tests
    testInstructorID = "INS001"
    testNonexistentInstructorID = "INS002"
    testInstructorName = "Test Instructor2"
    expectedKeys = [
        "name",
        "courseID",
        "secID",
        "term"
    ]

    def test_courseListInstructor(self):
        """Checks function returns course list of a given instructor."""
        # get keys from returned evalResponses
        keys = [key for key in getCourseListInstructor(self.testInstructorID)[0].keys()]
        # check keys are the same
        assert keys == self.expectedKeys

    def test_courseListInstructorNoEvals(self):
        """Checks function returns error message for given instructor with no evaluations."""
        # check keys are the same
        assert getCourseListInstructor(self.testNonexistentInstructorID) == f"No courses found for {self.testInstructorName}."



class Test_getCourseListDeptChair:
    """
    Tests for function getCourseListDeptChair.

    written by Carrie.
    """
    # variables for tests
    testDeptChairID = "DEP001"
    testNonexistentDeptChairID = "DEP002"
    testDeptChairName = "Test DeptChair2"
    expectedKeys = [
        "name",
        "courseID",
        "secID",
        "term"
    ]

    def test_courseListDeptChair(self):
        """Checks function returns course list of a given dept chair."""
        # get keys from returned evalResponses
        keys = [key for key in getCourseListDeptChair(self.testDeptChairID)[0].keys()]
        # check keys are the same
        assert keys == self.expectedKeys

    def test_courseListDeptChairNoEvals(self):
        """Checks function returns error message for given dept chair with no evaluations."""
        # check keys are the same
        assert getCourseListDeptChair(self.testNonexistentDeptChairID) == f"No courses found for {self.testDeptChairName}."

class Test_getCourseName:
    """
    Tests for function getCourseName.

    written by Carrie.
    """
    # variables for tests
    testCourseID = 530
    testNonexistentCourseID = 0
    expectedCourseName = "Software Engineering Methodology"

    def test_courseExists(self):
        """Checks correct course name is returned for a given course."""
        assert getCourseName(self.testCourseID) == self.expectedCourseName

    def test_courseNotExists(self):
        """Checks error message is returned for a given course that does not exist."""
        assert getCourseName(self.testNonexistentCourseID) == f"No course name found for {self.testNonexistentCourseID}."
