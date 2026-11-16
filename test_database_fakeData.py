# My compsci sever password is no longer working when connecting through VS code and I do not know what happened... 
# I am going to go to IT on Monday, but I did some mock testing in the meantime! 
#
# Tests for database functions
    # written by faith

from unittest.mock import Mock, patch
import database


# Check that a user is added with the correct information
def test_createUser():
    fakeDB = Mock()
    fakeCursor = Mock()
    fakeDB.cursor.return_value = fakeCursor

    with patch("database.getDB", return_value=fakeDB):
        database.createUser("123456", "Jane", "Doe", "jane@school.edu", "stu")

    fakeCursor.execute.assert_called_once()
    query, values = fakeCursor.execute.call_args[0]

    assert "INSERT INTO `user`" in query
    assert values == ("123456", "Jane", "Doe", "jane@school.edu", "stu")
    fakeDB.commit.assert_called_once()

# Check that 10 standard questions are sent to the database
def test_addStandardQuestions():
    fakeDB = Mock()
    fakeCursor = Mock()
    fakeDB.cursor.return_value = fakeCursor

    with patch("database.getDB", return_value=fakeDB):
        database.add_standardQuestions("TEST-EVAL")

    fakeCursor.executemany.assert_called_once()
    query, questions = fakeCursor.executemany.call_args[0]

    assert "INSERT INTO formField" in query
    assert len(questions) == 10

    # Check that all questions belong to the correct evaluation
    for question in questions:
        assert question[1] == "TEST-EVAL"

    fakeDB.commit.assert_called_once()


# Check that an existing question can be edited
def test_editExistingQuestion():
    fakeDB = Mock()
    fakeCursor = Mock()
    fakeDB.cursor.return_value = fakeCursor
    fakeCursor.rowcount = 1

    with patch("database.getDB", return_value=fakeDB):
        result = database.edit_evaluationQuestion(
            "TEST-EVAL", 1, "Updated question?", "shortText", "course", None
        )

    query, values = fakeCursor.execute.call_args[0]

    assert "UPDATE formField" in query
    assert values == ("Updated question?", "shortText", "course", None, "TEST-EVAL", 1)
    assert result == 1
    fakeDB.commit.assert_called_once()


# Check that editing a nonexistent question returns 0
def test_editNonexistentQuestion():
    fakeDB = Mock()
    fakeCursor = Mock()
    fakeDB.cursor.return_value = fakeCursor
    fakeCursor.rowcount = 0

    with patch("database.getDB", return_value=fakeDB):
        result = database.edit_evaluationQuestion(
            "DNE-EVAL", 444, "Updated question?", "shortText", "course", None
        )

    assert result == 0
