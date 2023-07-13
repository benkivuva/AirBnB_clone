#!/usr/bin/python3
"""Unit tests for state class"""

import unittest
import models
from models.state import State
from datetime import datetime
from time import sleep
import os


class Test_Review(unittest.TestCase):
    """Test casess for Place class"""

    def setUp(self):
        """Set up the env before each test case"""
        self.state = State()

    def tearDown(self):
        """Clean up the test env after each test case if needed"""
        pass

    def test_init_with_arguments(self):
        """Test initialization with arguments"""
        data = {
            'id': '123',
            'created_at': '2023-01-01T00:00:00',
            'updated_at': '2023-01-01T00:00:00',
            'name': 'Test'
        }
        self.state = State(**data)

        # Verify that the attributes are set correctly
        self.assertEqual(self.state.id, '123')
        self.assertEqual(self.state.created_at,
                         datetime.fromisoformat('2023-01-01T00:00:00'))
        self.assertEqual(self.state.updated_at,
                         datetime.fromisoformat('2023-01-01T00:00:00'))
        self.assertEqual(self.state.name, 'Test')

    def test_init_without_arguments(self):
        """Test initialization without arguments"""
        self.state = State()

        # Verify that the attributes are set correctly
        self.assertIsNotNone(self.state.id)
        self.assertIsNotNone(self.state.created_at)
        self.assertIsNotNone(self.state.updated_at)
        self.assertEqual(self.state.created_at, self.state.updated_at)

    def test_args(self):
        """Testing args which was unused"""
        st = State(None)
        self.assertNotIn(None, st.__dict__.values())

    def test_with_kwargs(self):
        """Testing with kwargs"""
        date = datetime.now()
        tform = date.isoformat()
        st = State(id="123", created_at=tform, updated_at=tform)
        self.assertEqual(st.id, "123")
        self.assertEqual(st.created_at, date)
        self.assertEqual(st.updated_at, date)

    def test_kwargs_None(self):
        """Testing with kwargs at None"""
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)

    def test_with_args_and_kwargs(self):
        """ testing with both args and kwargs"""
        date = datetime.now()
        tform = date.isoformat()
        st = State(id="123", created_at=tform, updated_at=tform)
        self.assertEqual(st.id, "123")
        self.assertEqual(st.created_at, date)
        self.assertEqual(st.updated_at, date)

    def test_id_is_str(self):
        """checks if id data type"""
        self.assertEqual(str, type(State().id))

    def test_id_is_unique(self):
        """test if ids generated are unique"""
        user1 = State()
        user2 = State()
        self.assertNotEqual(user1.id, user2.id)

    def test_created_at_datetime(self):
        """Checks if the attribute is a datetime object"""
        self.assertEqual(datetime, type(State().created_at))

    def test_created_at_timestamp(self):
        """checks if the timestamp is different"""
        user1 = State()
        sleep(0.05)
        user2 = State()
        self.assertLess(user1.created_at, user2.created_at)

    def test_updated_at_datetime(self):
        """Checks if attribute is a datetime object"""
        self.assertEqual(datetime, type(State(). updated_at))

    def test_updated_at_timestamp(self):
        """Checks if the timestamp is different"""
        user1 = State()
        sleep(0.05)
        user2 = State()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_instance_storage(self):
        """checks if storage and retrival were successful"""
        self.assertIn(State(), models.storage.all().values())

    def test__str__(self):
        """tests the string representation"""
        st1 = State()
        st2 = State()
        self.assertNotEqual(st1.__str__(), st2.__str__())

    def test_save(self):
        """tests the effectivity of timestamp updates"""
        st = State()
        sleep(0.1)
        update = st.updated_at
        st.save()
        self.assertLess(update, st.updated_at)

    def test_two_saves(self):
        """tests the effectivity of different timestamps updates"""
        st = State()
        sleep(0.1)
        upadte1 = st.updated_at
        st.save()
        update2 = st.updated_at
        self.assertLess(upadte1, update2)
        sleep(0.1)
        st.save()
        self.assertLess(update2, st.updated_at)

    def test_save_updates_file(self):
        """tests that updates are updated and stored correctly"""
        st = State()
        st.save()
        stid = "State." + st.id
        with open("file.json", "r") as file:
            self.assertIn(stid, file.read())

    def test_to_dict(self):
        """Tests the expected output"""
        expected_dict = {
            'id': self.state.id,
            'created_at': self.state.created_at.isoformat(),
            'updated_at': self.state.updated_at.isoformat(),
            '__class__': 'State'
        }
        self.assertEqual(self.state.to_dict(), expected_dict)

    def test_to_dict_type(self):
        """verifys the class returns a dictionary"""
        st = State()
        self.assertTrue(dict, type(st.to_dict()))

    def test_different_to_dict(self):
        """tests that the class produces 2 diff dict for diff instances"""
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertNotEqual(st1.to_dict(), st2.to_dict())

    def test_to_dict_has_correct_keys(self):
        """tests that the dict contains the right keys"""
        st = State()
        self.assertIn("id", st.to_dict())
        self.assertIn("__class__", st.to_dict())
        self.assertIn("created_at", st.to_dict())
        self.assertIn("updated_at", st.to_dict())

    def test_to_dict_created_at_format(self):
        """checks the ISO formatted string"""
        st = self.state.to_dict()
        created_at = st["created_at"]
        self.assertEqual(created_at, self.state.created_at.isoformat())

    def test_to_dict_updated_at_format(self):
        """checks the ISO formatted string"""
        st = self.state.to_dict()
        updated_at = st["updated_at"]
        self.assertEqual(updated_at, self.state.updated_at.isoformat())


if __name__ == "__main__":
    unittest.main()
