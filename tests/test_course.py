"""
Test functions related to courses.
"""

from database import getCourseDept

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