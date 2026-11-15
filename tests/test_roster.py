"""
Test functions related to roster.
"""

from database import getRoster

class Test_getRoster:
    """Tests for function getRoster."""
    testSecID = 50
    testCourseID = 530
    testTerm = "F26"
    expectedKeys = ["studentID", "firstName", "lastName", "email"]

    def test_getRoster(self): # written by Carrie
        """Checks function returns correct data based on retrieved dict keys."""
        # get keys from first returned dict
        keys = [key for key in getRoster(self.testSecID, self.testCourseID, self.testTerm)[0].keys()]
        assert keys == self.expectedKeys

    """TODO: @Ryan- write some unit test for alt paths for getRoster."""
