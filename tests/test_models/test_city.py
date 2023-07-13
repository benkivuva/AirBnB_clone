#!/usr/bin/python3
"""Unit tests for city class"""

import unittest
import models
from models.city import City
from datetime import datetime
from time import sleep
import os


class Test_City(unittest.TestCase):
    """Test casess for City class"""

    def setUp(self):
        """Set up the env before each test case"""
        self.city = City()

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
        self.city = City(**data)

        # Verify that the attributes are set correctly
        self.assertEqual(self.city.id, '123')
        self.assertEqual(self.city.created_at,
                         datetime.fromisoformat('2023-01-01T00:00:00'))
        self.assertEqual(self.city.updated_at,
                         datetime.fromisoformat('2023-01-01T00:00:00'))
        self.assertEqual(self.city.name, 'Test')

    def test_init_without_arguments(self):
        """Test initialization without arguments"""
        self.city = City()

        # Verify that the attributes are set correctly
        self.assertIsNotNone(self.city.id)
        self.assertIsNotNone(self.city.created_at)
        self.assertIsNotNone(self.city.updated_at)
        self.assertEqual(self.city.created_at, self.city.updated_at)

    def test_args(self):
        """Testing args which was unused"""
        cty = City(None)
        self.assertNotIn(None, cty.__dict__.values())

    def test_with_kwargs(self):
        """Testing with kwargs"""
        date = datetime.now()
        tform = date.isoformat()
        cty = City(id="123", created_at=tform, updated_at=tform)
        self.assertEqual(cty.id, "123")
        self.assertEqual(cty.created_at, date)
        self.assertEqual(cty.updated_at, date)

    def test_kwargs_None(self):
        """Testing with kwargs at None"""
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)

    def test_with_args_and_kwargs(self):
        """ testing with both args and kwargs"""
        date = datetime.now()
        tform = date.isoformat()
        cty = City(id="123", created_at=tform, updated_at=tform)
        self.assertEqual(cty.id, "123")
        self.assertEqual(cty.created_at, date)
        self.assertEqual(cty.updated_at, date)

    def test_id_is_str(self):
        """checks if id data type"""
        self.assertEqual(str, type(City().id))

    def test_id_is_unique(self):
        """test if ids generated are unique"""
        user1 = City()
        user2 = City()
        self.assertNotEqual(user1.id, user2.id)

    def test_created_at_datetime(self):
        """Checks if the attribute is a datetime object"""
        self.assertEqual(datetime, type(City().created_at))

    def test_created_at_timestamp(self):
        """checks if the timestamp is different"""
        user1 = City()
        sleep(0.05)
        user2 = City()
        self.assertLess(user1.created_at, user2.created_at)

    def test_updated_at_datetime(self):
        """Checks if attribute is a datetime object"""
        self.assertEqual(datetime, type(City(). updated_at))

    def test_updated_at_timestamp(self):
        """Checks if the timestamp is different"""
        user1 = City()
        sleep(0.05)
        user2 = City()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_instance_storage(self):
        """checks if storage and retrival were successful"""
        self.assertIn(City(), models.storage.all().values())

    def test__str__(self):
        """tests the string representation"""
        cty1 = City()
        cty2 = City()
        self.assertNotEqual(cty1.__str__(), cty2.__str__())

    def test_save(self):
        """tests the effectivity of timestamp updates"""
        cty = City()
        sleep(0.1)
        update = cty.updated_at
        cty.save()
        self.assertLess(update, cty.updated_at)

    def test_two_saves(self):
        """tests the effectivity of different timestamps updates"""
        cty = City()
        sleep(0.1)
        upadte1 = cty.updated_at
        cty.save()
        update2 = cty.updated_at
        self.assertLess(upadte1, update2)
        sleep(0.1)
        cty.save()
        self.assertLess(update2, cty.updated_at)

    def test_save_updates_file(self):
        """tests that updates are updated and stored correctly"""
        cty = City()
        cty.save()
        ctyid = "City." + cty.id
        with open("file.json", "r") as file:
            self.assertIn(ctyid, file.read())

    def test_to_dict(self):
        """Tests the expected output"""
        expected_dict = {
            'id': self.city.id,
            'created_at': self.city.created_at.isoformat(),
            'updated_at': self.city.updated_at.isoformat(),
            '__class__': 'City'
        }
        self.assertEqual(self.city.to_dict(), expected_dict)

    def test_to_dict_type(self):
        """verifys the class returns a dictionary"""
        cty = City()
        self.assertTrue(dict, type(cty.to_dict()))

    def test_different_to_dict(self):
        """tests that the class produces 2 diff dict for diff instances"""
        cty1 = City()
        sleep(0.05)
        cty2 = City()
        self.assertNotEqual(cty1.to_dict(), cty2.to_dict())

    def test_to_dict_has_correct_keys(self):
        """tests that the dict contains the right keys"""
        cty = City()
        self.assertIn("id", cty.to_dict())
        self.assertIn("__class__", cty.to_dict())
        self.assertIn("created_at", cty.to_dict())
        self.assertIn("updated_at", cty.to_dict())

    def test_to_dict_created_at_format(self):
        """checks the ISO formatted string"""
        cty = self.city.to_dict()
        created_at = cty["created_at"]
        self.assertEqual(created_at, self.city.created_at.isoformat())

    def test_to_dict_updated_at_format(self):
        """checks the ISO formatted string"""
        cty = self.city.to_dict()
        updated_at = cty["updated_at"]
        self.assertEqual(updated_at, self.city.updated_at.isoformat())


if __name__ == "__main__":
    unittest.main()
