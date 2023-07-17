#!/usr/bin/python3
"""Unit tests for user class"""

import unittest
import models
from models.user import User
from datetime import datetime
from time import sleep
import os


class Test_User(unittest.TestCase):
    """Test casess for User class"""

    def setUp(self):
        """Set up the env before each test case"""
        self.user = User()

    def tearDown(self):
        """Clean up the test env after each test case if needed"""
        del self.user

    def test_instance_creation(self):
        """tests if an instance is created the right way"""
        self.assertIsInstance(self.user, User)

    def test_init_with_arguments(self):
        """Test initialization with arguments"""
        data = {
            'id': '123',
            'created_at': '2023-01-01T00:00:00',
            'updated_at': '2023-01-01T00:00:00',
            'name': 'Test'
        }
        self.user = User(**data)

        # Verify that the attributes are set correctly
        self.assertEqual(self.user.id, '123')
        self.assertEqual(self.user.created_at,
                         datetime.fromisoformat('2023-01-01T00:00:00'))
        self.assertEqual(self.user.updated_at,
                         datetime.fromisoformat('2023-01-01T00:00:00'))
        self.assertEqual(self.user.name, 'Test')

    def test_init_without_arguments(self):
        """Test initialization without arguments"""
        self.user = User()

        # Verify that the attributes are set correctly
        self.assertIsNotNone(self.user.id)
        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)
        self.assertEqual(self.user.created_at, self.user.updated_at)

    def test_args(self):
        """Testing args which was unused"""
        usr = User(None)
        self.assertNotIn(None, usr.__dict__.values())

    def test_with_kwargs(self):
        """Testing with kwargs"""
        date = datetime.now()
        tform = date.isoformat()
        usr = User(id="123", created_at=tform, updated_at=tform)
        self.assertEqual(usr.id, "123")
        self.assertEqual(usr.created_at, date)
        self.assertEqual(usr.updated_at, date)

    def test_kwargs_None(self):
        """Testing with kwargs at None"""
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

    def test_with_args_and_kwargs(self):
        """ testing with both args and kwargs"""
        date = datetime.now()
        tform = date.isoformat()
        usr = User(id="123", created_at=tform, updated_at=tform)
        self.assertEqual(usr.id, "123")
        self.assertEqual(usr.created_at, date)
        self.assertEqual(usr.updated_at, date)

    def test_attributes(self):
        """tests the attributes for class user"""
        self.assertTrue(hasattr(self.user, "email"))
        self.assertTrue(hasattr(self.user, "password"))
        self.assertTrue(hasattr(self.user, "first_name"))
        self.assertTrue(hasattr(self.user, "last_name"))

    def test_attributes_default_values(self):
        """test the default values of attributes"""
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    def test_id_is_str(self):
        """checks if id data type"""
        self.assertEqual(str, type(User().id))

    def test_id_is_unique(self):
        """test if ids generated are unique"""
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def test_created_at_datetime(self):
        """Checks if the attribute is a datetime object"""
        self.assertEqual(datetime, type(User().created_at))

    def test_created_at_timestamp(self):
        """checks if the timestamp is different"""
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def test_updated_at_datetime(self):
        """Checks if attribute is a datetime object"""
        self.assertEqual(datetime, type(User(). updated_at))

    def test_updated_at_timestamp(self):
        """Checks if the timestamp is different"""
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_instance_storage(self):
        """checks if storage and retrival were successful"""
        self.assertIn(User(), models.storage.all().values())

    def test__str__(self):
        """tests the string representation"""
        user_str = str(self.user)
        expec_str = "[User] ({}) {}".format(self.user.id, self.user.__dict__)
        self.assertEqual(user_str, expec_str)

    def test_save(self):
        """tests the effectivity of timestamp updates"""
        usr = User()
        sleep(0.1)
        update = usr.updated_at
        usr.save()
        self.assertLess(update, usr.updated_at)

    def test_two_saves(self):
        """tests the effectivity of different timestamps updates"""
        usr = User()
        sleep(0.1)
        upadte1 = usr.updated_at
        usr.save()
        update2 = usr.updated_at
        self.assertLess(upadte1, update2)
        sleep(0.1)
        usr.save()
        self.assertLess(update2, usr.updated_at)

    def test_save_updates_file(self):
        """tests that updates are updated and stored correctly"""
        usr = User()
        usr.save()
        usrid = "User." + usr.id
        with open("file.json", "r") as file:
            self.assertIn(usrid, file.read())

    def test_to_dict(self):
        """Tests the expected output"""
        expected_dict = {
            'id': self.user.id,
            'created_at': self.user.created_at.isoformat(),
            'updated_at': self.user.updated_at.isoformat(),
            '__class__': 'User'
        }
        self.assertEqual(self.user.to_dict(), expected_dict)

    def test_to_dict_type(self):
        """verifys the class returns a dictionary"""
        usr = User()
        self.assertTrue(dict, type(usr.to_dict()))

    def test_different_to_dict(self):
        """tests that the class produces 2 diff dict for diff instances"""
        usr1 = User()
        sleep(0.05)
        usr2 = User()
        self.assertNotEqual(usr1.to_dict(), usr2.to_dict())

    def test_to_dict_has_correct_keys(self):
        """tests that the dict contains the right keys"""
        usr = User()
        self.assertIn("id", usr.to_dict())
        self.assertIn("__class__", usr.to_dict())
        self.assertIn("created_at", usr.to_dict())
        self.assertIn("updated_at", usr.to_dict())

    def test_to_dict_created_at_format(self):
        """checks the ISO formatted string"""
        usr = self.user.to_dict()
        created_at = usr["created_at"]
        self.assertEqual(created_at, self.user.created_at.isoformat())

    def test_to_dict_updated_at_format(self):
        """checks the ISO formatted string"""
        usr = self.user.to_dict()
        updated_at = usr["updated_at"]
        self.assertEqual(updated_at, self.user.updated_at.isoformat())

    def test_to_dict_method(self):
        """test to_dict method of user"""
        user_dict = self.user.to_dict()
        self.assertIsInstance(user_dict, dict)
        self.assertEqual(user_dict['__class__'], 'User')
        self.assertTrue('id' in user_dict)
        self.assertTrue('created_at' in user_dict)
        self.assertTrue('updated_at' in user_dict)


if __name__ == "__main__":
    unittest.main()
