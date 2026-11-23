"""
Test functions related to users.
"""

from constants import ROLE
from database import getDept, getInstructorByCourse, getRoleID, getUserRole


class Test_getUserRole:
    """
    Tests for function getUserRole.
    
    written by Carrie.
    """
    # variables for mutliple tests
    # IDs for userID (DB ID)
    testStudentID = "STU001"
    testInstructorID = "INS001"
    testDeptChairID = "DEP001"
    testAdminID = "ADM001"
    testNonexistentID = "DNE000"
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

    def test_NonexistentID(self):
        """Check that function returns error msg for userID that does not exist."""
        assert getUserRole(self.testNonexistentID) == f"No role found for userID '{self.testNonexistentID}'."

    def test_blankID(self):
        """Check that function returns error msg for empty userID."""
        assert getUserRole(self.testEmptyID) == f"No role found for userID '{self.testEmptyID}'."


class Test_getRoleID:
    """
    Tests for function getUserRole.

    written by Carrie.
    """
    # variables for mutliple tests
    testStudentID = "STU001"
    testInstructorID = "INS001"
    testDeptChairID = "DEP001"
    testAdminID = "ADM001"
    testNonexistentID = "DNE000"
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

    def test_NonexistentID(self):
        """Check that function returns error msg for userID that does not exist."""
        assert getRoleID(self.testNonexistentID) == f"No specialized role ID for userID '{self.testNonexistentID}'."

    def test_blankID(self):
        """Check that function returns error msg for empty userID."""
        assert getRoleID(self.testEmptyID) == f"No specialized role ID for userID '{self.testEmptyID}'."

class Test_getDept:
    """
    Tests for function getDept.

    written by Carrie.
    """
    # variables for tests
    testInstructorID = "INS001"
    testDeptChairID = "DEP001"
    testNonexistentID = "DNE000"
    testEmptyID = ""

    dept = 145
    
    def test_getInstrustorDept(self):
        """Check that function returns correct dept for instructor in instructor table."""
        assert getDept(self.testInstructorID) == self.dept

    def test_getDeptChairDept(self):
        """Check that function returns correct dept for dept chair in instructor table."""
        assert getDept(self.testDeptChairID) == self.dept

    def test_getNonexistentIDDept(self):
        """Check that function returns error message for Nonexistent ID."""
        assert getDept(self.testNonexistentID) == f"No dept found for userID '{self.testNonexistentID}'."

    def test_getEmptyIDDept(self):
        """Check that function returns error message for empty ID."""
        assert getDept(self.testEmptyID) == f"No dept found for userID '{self.testEmptyID}'."


class Test_getInstructorByCourse:
    """
    Tests for functionget InstructorByCourse

    written by Carrie.
    """
    # variables for tests
    testCourseID = 530
    testSecID = 50
    testNoInstructorSecID = 51
    testTerm = 'F26'
    testInstructorID = "INS001"

    def test_InstructorExists(self):
        """Check that function returns instructor given a course."""
        assert getInstructorByCourse(self.testCourseID, self.testSecID, self.testTerm) == self.testInstructorID

    def test_NoInstructorExists(self):
        """Check that function returns error message if no instructor exists for given a course."""
        assert getInstructorByCourse(
            self.testCourseID, 
            self.testNoInstructorSecID, 
            self.testTerm
            ) == f"No instructor found for {self.testCourseID}-{self.testNoInstructorSecID}-{self.testTerm}."
