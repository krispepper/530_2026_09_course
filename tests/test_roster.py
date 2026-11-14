import pytest
from database import getRoster

class Test_getRoster:
    """Tests for function getRoster"""
    testSecID = 50
    testCourseID = 530
    testTerm = "F26"

    def test_getRoster(self):
        print(getRoster(self.testSecID, self.testCourseID, self.testTerm))
        assert getRoster(self.testSecID, self.testCourseID, self.testTerm) == []
