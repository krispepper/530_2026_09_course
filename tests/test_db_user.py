import pytest
from database import getUserRole, getRoleID, getDept
from constants import ROLE

class Test_getUserRole:
    """Tests for function getUserRole."""
    # variables for mutliple tests
    # IDs for userID (DB ID)
    testStudentID = "STU001"
    testInstructorID = "INS001"
    testDeptChairID = "DEP001"
    testAdminID = "ADM001"
    testNonexistantD = "DNE000"
    testEmptyID = ""

    def test_studentRole(self):
        """Check that function returns role 'stu' for user in student table."""
        assert getUserRole(self.testStudentID) == ROLE.student.value

    def test_instructorRole(self):
        """Check that function returns role 'ins' for user in instructor table."""
        assert getUserRole(self.testInstructorID) == ROLE.instructor.value

    def test_deptChairRole(self):
        """Check that function returns role 'dc' for user in deptChair table."""
        assert getUserRole(self.testDeptChairID) == ROLE.deptChair.value

    def test_schoolAdminRole(self):
        """Check that function returns role 'sca' for user in schoolAdmin table."""
        assert getUserRole(self.testAdminID) == ROLE.schoolAdmin.value

    def test_nonexistantID(self):
        """Check that function returns error msg for userID that does not exist."""
        assert getUserRole(self.testNonexistantD) == f"No role found for userID '{self.testNonexistantD}'."

    def test_blankID(self):
        """Check that function returns error msg for empty userID."""
        assert getUserRole(self.testEmptyID) == f"No role found for userID '{self.testEmptyID}'."


class Test_getRoleID:
    """Tests for function getUserRole."""
    # variables for mutliple tests
    testStudentID = "STU001"
    testInstructorID = "INS001"
    testDeptChairID = "DEP001"
    testAdminID = "ADM001"
    testNonexistantD = "DNE000"
    testEmptyID = ""

    # IDs for user roles (school related IDs)
    testStudentRoleID = "9886690" 
    testInstructorRoleID = "9638329"
    testDeptChairRoleID = "8507749"
    testAdminRoleID = "9940062"
    
    def test_studentRole(self):
        """Check that function returns correct studentID for user in student table."""
        assert getRoleID(self.testStudentID) == self.testStudentRoleID

    def test_instructorRole(self):
        """Check that function returns correct instructorID for user in instructor table."""
        assert getRoleID(self.testInstructorID) == self.testInstructorRoleID

    def test_deptChairRole(self):
        """Check that function returns correct instructorID for user in deptChair table."""
        assert getRoleID(self.testDeptChairID) == self.testDeptChairRoleID

    def test_schoolAdminRole(self):
        """Check that function returns correct adminID for user in schoolAdmin table."""
        assert getRoleID(self.testAdminID) == self.testAdminRoleID

    def test_nonexistantID(self):
        """Check that function returns error msg for userID that does not exist."""
        assert getRoleID(self.testNonexistantD) == f"No specialized role ID for userID '{self.testNonexistantD}'."

    def test_blankID(self):
        """Check that function returns error msg for empty userID."""
        assert getRoleID(self.testEmptyID) == f"No specialized role ID for userID '{self.testEmptyID}'."

class Test_getDept:
    """Tests for function getDept."""
    # variables for tests
    testInstructorID = "INS001"
    testDeptChairID = "DEP001"
    testNonexistantD = "DNE000"
    testEmptyID = ""

    dept = 145
    
    def test_getInstrustorDept(self):
        """Check that function returns correct dept for instructor in instructor table."""
        assert getDept(self.testInstructorID) == self.dept

    def test_getDeptChairDept(self):
        """Check that function returns correct dept for dept chair in instructor table."""
        assert getDept(self.testDeptChairID) == self.dept

    def test_getNonexistantIDDept(self):
        """Check that function returns error message for nonexistant ID."""
        assert getDept(self.testNonexistantDt) == f"No dept found for userID '{self.testNonexistantD}'."

    def test_getNonexistantIDDept(self):
        """Check that function returns error message for empty ID."""
        assert getDept(self.testEmptyID) == f"No dept found for userID '{self.testEmptyID}'."