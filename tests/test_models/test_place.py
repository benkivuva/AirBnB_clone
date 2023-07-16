#!/usr/bin/python3
"""Unit tests for place class"""

import unittest
import models
from models.place import Place
from datetime import datetime
from time import sleep
import os


class Test_Review(unittest.TestCase):
    """Test casess for Place class"""

    def setUp(self):
        """Set up the env before each test case"""
        self.place = Place()

    def tearDown(self):
        """Clean up the test env after each test case if needed"""
        self.place = None

    def test_init_with_arguments(self):
        """Test initialization with arguments"""
        data = {
            'id': '123',
            'created_at': '2023-01-01T00:00:00',
            'updated_at': '2023-01-01T00:00:00',
            'name': 'Test'
        }
        self.place = Place(**data)

        # Verify that the attributes are set correctly
        self.assertEqual(self.place.id, '123')
        self.assertEqual(self.place.created_at,
                         datetime.fromisoformat('2023-01-01T00:00:00'))
        self.assertEqual(self.place.updated_at,
                         datetime.fromisoformat('2023-01-01T00:00:00'))
        self.assertEqual(self.place.name, 'Test')

    def test_init_without_arguments(self):
        """Test initialization without arguments"""
        self.place = Place()

        # Verify that the attributes are set correctly
        self.assertIsNotNone(self.place.id)
        self.assertIsNotNone(self.place.created_at)
        self.assertIsNotNone(self.place.updated_at)
        self.assertEqual(self.place.created_at, self.place.updated_at)

    def test_args(self):
        """Testing args which was unused"""
        pl = Place(None)
        self.assertNotIn(None, pl.__dict__.values())

    def test_with_kwargs(self):
        """Testing with kwargs"""
        date = datetime.now()
        tform = date.isoformat()
        pl = Place(id="123", created_at=tform, updated_at=tform)
        self.assertEqual(pl.id, "123")
        self.assertEqual(pl.created_at, date)
        self.assertEqual(pl.updated_at, date)

    def test_kwargs_None(self):
        """Testing with kwargs at None"""
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)

    def test_with_args_and_kwargs(self):
        """ testing with both args and kwargs"""
        date = datetime.now()
        tform = date.isoformat()
        pl = Place(id="123", created_at=tform, updated_at=tform)
        self.assertEqual(pl.id, "123")
        self.assertEqual(pl.created_at, date)
        self.assertEqual(pl.updated_at, date)

    def test_attributes_initialization(self):
        """tests atrr initialization"""
        self.assertEqual(self.place.city_id, "")
        self.assertEqual(self.place.user_id, "")
        self.assertEqual(self.place.name, "")
        self.assertEqual(self.place.description, "")
        self.assertEqual(self.place.number_rooms, 0)
        self.assertEqual(self.place.number_bathrooms, 0)
        self.assertEqual(self.place.max_guest, 0)
        self.assertEqual(self.place.price_by_night, 0)
        self.assertEqual(self.place.latitude, 0.0)
        self.assertEqual(self.place.longitude, 0.0)
        self.assertEqual(self.place.amenity_ids, [])
        self.assertTrue(hasattr(self.place, "id"))
        self.assertTrue(hasattr(self.place, "created_at"))
        self.assertTrue(hasattr(self.place, "updated_at"))

    def test_id_is_str(self):
        """checks if id data type"""
        self.assertEqual(str, type(Place().id))

    def test_id_is_unique(self):
        """test if ids generated are unique"""
        user1 = Place()
        user2 = Place()
        self.assertNotEqual(user1.id, user2.id)

    def test_created_at_datetime(self):
        """Checks if the attribute is a datetime object"""
        self.assertEqual(datetime, type(Place().created_at))

    def test_created_at_timestamp(self):
        """checks if the timestamp is different"""
        user1 = Place()
        sleep(0.05)
        user2 = Place()
        self.assertLess(user1.created_at, user2.created_at)

    def test_updated_at_datetime(self):
        """Checks if attribute is a datetime object"""
        self.assertEqual(datetime, type(Place(). updated_at))

    def test_updated_at_timestamp(self):
        """Checks if the timestamp is different"""
        user1 = Place()
        sleep(0.05)
        user2 = Place()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_instance_storage(self):
        """checks if storage and retrival were successful"""
        self.assertIn(Place(), models.storage.all().values())

    def test__str__(self):
        """tests the string representation"""
        pl1 = Place()
        pl2 = Place()
        self.assertNotEqual(pl1.__str__(), pl2.__str__())

    def test__str__method(self):
        """tests the str method"""
        pl_str = str(self.place)
        self.assertIn("[Place]", pl_str)
        self.assertIn("id", pl_str)
        self.assertIn("created_at", pl_str)
        self.assertIn("updated_at", pl_str)

    def test_save(self):
        """tests the effectivity of timestamp updates"""
        pl = Place()
        sleep(0.1)
        update = pl.updated_at
        pl.save()
        self.assertLess(update, pl.updated_at)

    def test_two_saves(self):
        """tests the effectivity of different timestamps updates"""
        pl = Place()
        sleep(0.1)
        upadte1 = pl.updated_at
        pl.save()
        update2 = pl.updated_at
        self.assertLess(upadte1, update2)
        sleep(0.1)
        pl.save()
        self.assertLess(update2, pl.updated_at)

    def test_save_updates_file(self):
        """tests that updates are updated and stored correctly"""
        pl = Place()
        pl.save()
        plid = "Place." + pl.id
        with open("file.json", "r") as file:
            self.assertIn(plid, file.read())

    def test_save_method(self):
        """tests the save() method"""
        updated_at_1 = self.place.updated_at
        self.place.save()
        updated_at_2 = self.place.updated_at
        self.assertNotEqual(updated_at_1, updated_at_2)

    def test_to_dict(self):
        """Tests the expected output"""
        expected_dict = {
            'id': self.place.id,
            'created_at': self.place.created_at.isoformat(),
            'updated_at': self.place.updated_at.isoformat(),
            '__class__': 'Place'
        }
        self.assertEqual(self.place.to_dict(), expected_dict)

    def test_to_dict_type(self):
        """verifys the class returns a dictionary"""
        pl = Place()
        self.assertTrue(dict, type(pl.to_dict()))

    def test_different_to_dict(self):
        """tests that the class produces 2 diff dict for diff instances"""
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        self.assertNotEqual(pl1.to_dict(), pl2.to_dict())

    def test_to_dict_has_correct_keys(self):
        """tests that the dict contains the right keys"""
        pl = Place()
        self.assertIn("id", pl.to_dict())
        self.assertIn("__class__", pl.to_dict())
        self.assertIn("created_at", pl.to_dict())
        self.assertIn("updated_at", pl.to_dict())

    def test_to_dict_created_at_format(self):
        """checks the ISO formatted string"""
        pl = self.place.to_dict()
        created_at = pl["created_at"]
        self.assertEqual(created_at, self.place.created_at.isoformat())

    def test_to_dict_updated_at_format(self):
        """checks the ISO formatted string"""
        pl = self.place.to_dict()
        updated_at = pl["updated_at"]
        self.assertEqual(updated_at, self.place.updated_at.isoformat())


if __name__ == "__main__":
    unittest.main()
