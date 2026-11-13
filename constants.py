"""
Constants for app.
"""
import enum


class ROLE(enum.Enum):
    """User roles."""
    student = "stu"
    instructor = "ins"
    deptChair = "dc"
    schoolAdmin = "aca"
