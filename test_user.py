# This file is to test creating users 
    # written by faith 

import pytest
import app as app_module
from unittest.mock import patch

# Tests for "add_user()" from app.py (which calls createUser() from database.py)
class Test_addUser:

    # Variables for multiple tests
    testUserData = {"userID": "123456",
                    "firstName": "Jane",
                    "lastName": "Doe",
                    "email": "janeDoe@school.edu",
                    "role": "stu"
                   }

    testMissingFields = ["userID", "firstName", "lastName", "email", "role"]

    # Check that a user can be successfully created with valid information
    def test_validUser(self):
        user_data = self.testUserData.copy()

        with patch("app.createUser") as mock_createUser:
                test_app = app_module.app.test_client()
                response = test_app.post("/users", json=user_data)

        assert response.status_code == 201
        assert response.get_json() == {"message": "User was successfully created"}
        mock_createUser.assert_called_once_with(
            "123456", "Jane", "Doe", "janeDoe@school.edu", "stu"
        )

    # Check that a user cannot be created with missing fields.
    def test_missingFields(self):
        for field in self.testMissingFields:
            user_data = self.testUserData.copy()
            user_data.pop(field)

            test_app = app_module.app.test_client()
            response = test_app.post("/users", json=user_data)

            assert response.status_code == 400

    # Check that a user cannot be created with empty fields.
    def test_emptyFields(self):
        for field in self.testMissingFields:
            user_data = self.testUserData.copy()
            user_data[field] = ""

            test_app = app_module.app.test_client()
            response = test_app.post("/users", json=user_data)

            assert response.status_code == 400

    # Check that a user cannot be created with an invalid role.
    def test_invalidRole(self):
        user_data = self.testUserData.copy()
        user_data["role"] = "student"

        test_app = app_module.app.test_client()
        response = test_app.post("/users", json=user_data)

        assert response.status_code == 400

    # Check that a user cannot be created with an invalid email.
    def test_invalidEmail(self):
        user_data = self.testUserData.copy()
        user_data["email"] = "blahblahblah"

        test_app = app_module.app.test_client()
        response = test_app.post("/users", json=user_data)

        assert response.status_code == 400