# Tests for getUserNameFromId were all written by Hugo.
# Test used for M4 Unit Test assignment submission is test_validId; written by Hugo.
from database import getUserNameFromId


# Tests the function getUserNameFromId.
class Test_getUserNameFromId:
    testValidId = "ADM001" # present in database
    testNonexistantId = "STU999" # not present in database
    testBadFormatId = "xxxxXX" # 6 characters, but improperly formatted
    testShortId = "INS00" # 5 characters
    testLongId = "DEP0011" # 7 characters
    testEmptyId = "" # empty

    def test_validId(self):
        """Check that the function returns the dictionary {firstName:"Test",lastName:"Admin"}."""
        assert getUserNameFromId(self.testValidId) == {"firstName": "Test", "lastName": "Admin"}

    def test_NonexistantId(self):
        """Check that the function returns an error msg for a userID that does not exist."""
        assert getUserNameFromId(self.testNonexistantId) == f"User not found with userID of: '{self.testNonexistantId}'."

    def test_BadFormatId(self):
        """Check that the function returns an error msg for an improperly formatted userID."""
        assert getUserNameFromId(self.testBadFormatId) == f"User not found with userID of: '{self.testBadFormatId}'."

    def test_ShortId(self):
        """Check that the function returns an error msg for a userID that is too short."""
        assert getUserNameFromId(self.testShortId) == f"User not found with userID of: '{self.testShortId}'."

    def test_LongId(self):
        """Check that the function returns an error msg for a userID that is too long."""
        assert getUserNameFromId(self.testLongId) == f"User not found with userID of: '{self.testLongId}'."

    def test_EmptyId(self):
        """Check that the function returns an error msg for an empty userID."""
        assert getUserNameFromId(self.testEmptyId) == f"User not found with userID of: '{self.testEmptyId}'."