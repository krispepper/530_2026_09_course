"""
Test functions related to roster.
"""

from database import getRoster

class Test_getRoster:
    """Tests for function getRoster."""
    testSecID = 50
    testCourseID = 530
    testTerm = "F26"
    testNonexistantSec = 69
    testNonexistantCourse = 420
    testNonexistantTerm = "S23"
    expectedKeys = ["studentID", "firstName", "lastName", "email"]

    def test_getRoster(self): # written by Carrie
        """Checks function returns correct data based on retrieved dict keys."""
        # get keys from first returned dict
        keys = [key for key in getRoster(self.testSecID, self.testCourseID, self.testTerm)[0].keys()]
        assert keys == self.expectedKeys

    def test_nonexistantSec(self):
        """Checks function returns error message for nonexistant section ID"""
        assert getRoster(self.testNonexistantSec, self.testCourseID, self.testTerm) == "No enrollment found for course '{courseID}-{secID}-{term}'."
    
    def test_nonexistantCourse(self):
        """Checks function returns error message for nonexistant course ID"""
        assert getRoster(self.testSecID, self.testNonexistantCourse, self.testTerm) == "No enrollment found for course '{courseID}-{secID}-{term}'."
    
    def test_nonexistantTerm(self):
        """Checks function returns error message for nonexistant term"""
        assert getRoster(self.testSecID, self.testCourseID, self.testNonexistantTerm) == "No enrollment found for course '{courseID}-{secID}-{term}'."