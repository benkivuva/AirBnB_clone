#!/usr/bin/python3
"""Unit tests for BaseModel class"""

import unittest
import models
from models.base_model import BaseModel
from datetime import datetime
from time import sleep
import os


class Test_BaseModel(unittest.TestCase):
    """Test casess for BaseModel class"""

    def setUp(self):
        """Set up the env before each test case"""
        self.base_model = BaseModel()

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
        base_model = BaseModel(**data)

        # Verify that the attributes are set correctly
        self.assertEqual(base_model.id, '123')
        self.assertEqual(base_model.created_at,
                         datetime.fromisoformat('2023-01-01T00:00:00'))
        self.assertEqual(base_model.updated_at,
                         datetime.fromisoformat('2023-01-01T00:00:00'))
        self.assertEqual(base_model.name, 'Test')

    def test_init_without_arguments(self):
        """Test initialization without arguments"""
        base_model = BaseModel()

        # Verify that the attributes are set correctly
        self.assertIsNotNone(base_model.id)
        self.assertIsNotNone(base_model.created_at)
        self.assertIsNotNone(base_model.updated_at)
        self.assertEqual(base_model.created_at, base_model.updated_at)

    def test_args(self):
        """Testing args which was unused"""
        bm = BaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_with_kwargs(self):
        """Testing with kwargs"""
        date = datetime.now()
        tform = date.isoformat()
        bm = BaseModel(id="123", created_at=tform, updated_at=tform)
        self.assertEqual(bm.id, "123")
        self.assertEqual(bm.created_at, date)
        self.assertEqual(bm.updated_at, date)

    def test_kwargs_None(self):
        """Testing with kwargs at None"""
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_with_args_and_kwargs(self):
        """ testing with both args and kwargs"""
        date = datetime.now()
        tform = date.isoformat()
        bm = BaseModel(id="123", created_at=tform, updated_at=tform)
        self.assertEqual(bm.id, "123")
        self.assertEqual(bm.created_at, date)
        self.assertEqual(bm.updated_at, date)

    def test_id_is_str(self):
        """checks if id data type"""
        self.assertEqual(str, type(BaseModel().id))

    def test_id_is_unique(self):
        """test if id generated are unique"""
        user1 = BaseModel()
        user2 = BaseModel()
        self.assertNotEqual(user1.id, user2.id)

    def test_created_at_datetime(self):
        """Checks if the attribute is a datetime object"""
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_created_at_timestamp(self):
        """checks if the timestamp is different"""
        user1 = BaseModel()
        sleep(0.05)
        user2 = BaseModel()
        self.assertLess(user1.created_at, user2.created_at)

    def test_updated_at_datetime(self):
        """Checks if attribute is a datetime object"""
        self.assertEqual(datetime, type(BaseModel(). updated_at))

    def test_updated_at_timestamp(self):
        """Checks if the timestamp is different"""
        user1 = BaseModel()
        sleep(0.05)
        user2 = BaseModel()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_instance_storage(self):
        """checks if storage and retrival were successful"""
        self.assertIn(BaseModel(), models.storage.all().values())

    def test__str__(self):
        """tests the string representation"""
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm1.__str__(), bm2.__str__())

    def test_save(self):
        """tests the effective of timestamp updates"""
        bm = BaseModel()
        sleep(0.1)
        update = bm.updated_at
        bm.save()
        self.assertLess(update, bm.updated_at)

    def test_two_saves(self):
        """tests the effectivity of diffrent timestamps updates"""
        bm = BaseModel()
        sleep(0.1)
        upadte1 = bm.updated_at
        bm.save()
        update2 = bm.updated_at
        self.assertLess(upadte1, update2)
        sleep(0.1)
        bm.save()
        self.assertLess(update2, bm.updated_at)

    def test_save_updates_file(self):
        """tests that updates are updated and stored correctly"""
        bm = BaseModel()
        bm.save()
        bmid = "BaseModel." + bm.id
        with open("file.json", "r") as file:
            self.assertIn(bmid, file.read())

    def test_to_dict(self):
        """Tests the expected output"""
        expected_dict = {
            'id': self.base_model.id,
            'created_at': self.base_model.created_at.isoformat(),
            'updated_at': self.base_model.updated_at.isoformat(),
            '__class__': 'BaseModel'
        }
        self.assertEqual(self.base_model.to_dict(), expected_dict)

    def test_to_dict_type(self):
        """verifys the class returns a dictionary"""
        bm = BaseModel()
        self.assertTrue(dict, type(bm.to_dict()))

    def test_different_to_dict(self):
        """tests that the class produces 2 diff dict for diff instances"""
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        self.assertNotEqual(bm1.to_dict(), bm2.to_dict())

    def test_to_dict_has_correct_keys(self):
        """tests that the dict contains the right keys"""
        bm = BaseModel()
        self.assertIn("id", bm.to_dict())
        self.assertIn("__class__", bm.to_dict())
        self.assertIn("created_at", bm.to_dict())
        self.assertIn("updated_at", bm.to_dict())

    def test_to_dict_created_at_format(self):
        """checks the ISO formatted string"""
        bm = self.base_model.to_dict()
        created_at = bm["created_at"]
        self.assertEqual(created_at, self.base_model.created_at.isoformat())

    def test_to_dict_updated_at_format(self):
        """checks the ISO formatted string"""
        bm = self.base_model.to_dict()
        updated_at = bm["updated_at"]
        self.assertEqual(updated_at, self.base_model.updated_at.isoformat())


if __name__ == "__main__":
    unittest.main()
