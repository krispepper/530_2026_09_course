"""
Test functions related to roster.
"""

from database import canViewRoster, getRoster


class Test_getRoster:
    """Tests for function getRoster."""
    testSecID = 50
    testCourseID = 530
    testTerm = "F26"
    testNonexistentSec = 69
    testNonexistentCourse = 420
    testNonexistentTerm = "S23"
    expectedKeys = ["userID", "studentID", "firstName", "lastName", "email"]

    def test_getRoster(self): # written by Carrie
        """Checks function returns correct data based on retrieved dict keys."""
        # get keys from first returned dict
        keys = [key for key in getRoster(self.testSecID, self.testCourseID, self.testTerm)[0]]
        assert keys == self.expectedKeys

    def test_NonexistentSec(self): # written by Ryan
        """Checks function returns error message for nonexistent section ID"""
        assert getRoster(self.testNonexistentSec, self.testCourseID, self.testTerm) == (
            f"No enrollment found for course '{self.testCourseID}-{self.testNonexistentSec}-{self.testTerm}'."
            )
    
    def test_NonexistentCourse(self): # written by Ryan
        """Checks function returns error message for nonexistent course ID"""
        assert getRoster(self.testSecID, self.testNonexistentCourse, self.testTerm) == (
            f"No enrollment found for course '{self.testNonexistentCourse}-{self.testSecID}-{self.testTerm}'."
            )
    
    def test_NonexistentTerm(self): # written by Ryan
        """Checks function returns error message for nonexistent term"""
        assert getRoster(self.testSecID, self.testCourseID, self.testNonexistentTerm) == (
            f"No enrollment found for course '{self.testCourseID}-{self.testSecID}-{self.testNonexistentTerm}'."
            )


class Test_canViewRoster:
    """
    Tests function canViewRoster.
    """
    testCourseID = 530
    testSecID = 50
    testTerm = 'F26'
    returnedIDs = ['INS001', 'DEP001']
    testBadCourseID = 0
    testBadSecID = 0
    testBadTerm = 'F20'


    def test_accessAccepted(self):
        """checks expected userIDs are returned by function."""
        assert set(self.returnedIDs) == set(canViewRoster(self.testCourseID, self.testSecID, self.testTerm))

    def test_noOneWithAccess(self):
        """checks empty list is returned for a class with no dept chair or instructor assigned."""
        assert [] == canViewRoster(self.testBadCourseID, self.testBadSecID, self.testBadTerm)