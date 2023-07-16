#!/usr/bin/python3
"""Unittests for the FileStorage class"""

import unittest
import time
import json
import os
import re
import pep8
import models
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from datetime import datetime
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class Test_FileStorage(unittest.TestCase):
    """Unittest for class Filestorage attributes and methods"""

    @classmethod
    def setUp(self):
        """Sets up the env before each test case"""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """Clean up the test env after each test case if needed"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_pep8_conformance_FileStorage(self):
        """Test that file_storage.py file conform to PEP8"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/file_storage.py'])
        self.assertEqual(result.total_errors, 1,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_FileStorage(self):
        """Test that test_file_storage.py file conform to PEP8"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/\
                                        test_file_storage.py'])
        self.assertEqual(result.total_errors, 1,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """tests existence of docstrings in the modules"""
        self.assertTrue(len(FileStorage.__doc__) >= 1)

    def test_class_docstring(self):
        """tests existence of docstrings in the classes"""
        self.assertTrue(len(FileStorage.__doc__) >= 1)

    def test_instantiation_no_args(self):
        """
        tests if creating an obj without arguments returns
        an obj of the correct type
        """
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_instantiation_with_args(self):
        """tests if creating an obj with args return its correct type"""
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_attribute_filepath_is_private(self):
        """tests if the class attribute is a private string"""
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_attribute_objects_is_private(self):
        """tests if the class attribute is a private dictionary"""
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        """
        tests if models.storage obj is initialized
        as an instance of FileStorage
        """
        self.assertEqual(type(models.storage), FileStorage)

    def test_all(self):
        """tests if all() returns a dictionary"""
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_args(self):
        """test all with arguments returns a dict"""
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        """
        tests if new() correctly adds objects to the storage and that
        the added objects are present in the storage with the expected
        keys and values
        """
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        self.assertIn("BaseModel." + bm.id, models.storage.all().keys())
        self.assertIn(bm, models.storage.all().values())
        self.assertIn("User." + us.id, models.storage.all().keys())
        self.assertIn(us, models.storage.all().values())
        self.assertIn("State." + st.id, models.storage.all().keys())
        self.assertIn(st, models.storage.all().values())
        self.assertIn("Place." + pl.id, models.storage.all().keys())
        self.assertIn(pl, models.storage.all().values())
        self.assertIn("City." + cy.id, models.storage.all().keys())
        self.assertIn(cy, models.storage.all().values())
        self.assertIn("Amenity." + am.id, models.storage.all().keys())
        self.assertIn(am, models.storage.all().values())
        self.assertIn("Review." + rv.id, models.storage.all().keys())
        self.assertIn(rv, models.storage.all().values())

    def test_new_with_args(self):
        """tests new() with arguments"""
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_with_None(self):
        """tests new() with none"""
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save_with_arg(self):
        """tests save() with args"""
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_save(self):
        """
        tests that save() correctly serializes the objects and saves
        them to the specified file. Also checks whether the saved text contains
        the expected information for each object
        """
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + bm.id, save_text)
            self.assertIn("User." + us.id, save_text)
            self.assertIn("State." + st.id, save_text)
            self.assertIn("Place." + pl.id, save_text)
            self.assertIn("City." + cy.id, save_text)
            self.assertIn("Amenity." + am.id, save_text)
            self.assertIn("Review." + rv.id, save_text)

    def test_reload_with_arg(self):
        """tests reload with arguments"""
        with self.assertRaises(TypeError):
            models.storage.reload(None)

    def test_reload(self):
        """Tests that reload, reloads objects from string file"""
        a_storage = FileStorage()
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        with open("file.json", "w") as f:
            f.write("{}")
        with open("file.json", "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(a_storage.reload(), None)


if __name__ == "__main__":
    unittest.main()
