"""
Test functions related to roster.
"""

from database import getRoster

class Test_getRoster:
    """Tests for function getRoster."""
    testSecID = 50
    testCourseID = 530
    testTerm = "F26"
    testNonexistentSec = 69
    testNonexistentCourse = 420
    testNonexistentTerm = "S23"
    expectedKeys = ["studentID", "firstName", "lastName", "email"]

    def test_getRoster(self): # written by Carrie
        """Checks function returns correct data based on retrieved dict keys."""
        # get keys from first returned dict
        keys = [key for key in getRoster(self.testSecID, self.testCourseID, self.testTerm)[0].keys()]
        assert keys == self.expectedKeys

    def test_nonexistantSec(self): # written by Ryan
        """Checks function returns error message for nonexistent section ID"""
        assert getRoster(self.testNonexistentSec, self.testCourseID, self.testTerm) == (
            f"No enrollment found for course '{self.testCourseID}-{self.testNonexistentSec}-{self.testTerm}'."
            )
    
    def test_nonexistantCourse(self): # written by Ryan
        """Checks function returns error message for nonexistent course ID"""
        assert getRoster(self.testSecID, self.testNonexistentCourse, self.testTerm) == (
            f"No enrollment found for course '{self.testNonexistentCourse}-{self.testSecID}-{self.testTerm}'."
            )
    
    def test_nonexistantTerm(self): # written by Ryan
        """Checks function returns error message for nonexistent term"""
        assert getRoster(self.testSecID, self.testCourseID, self.testNonexistentTerm) == (
            f"No enrollment found for course '{self.testCourseID}-{self.testSecID}-{self.testNonexistentTerm}'."
            )