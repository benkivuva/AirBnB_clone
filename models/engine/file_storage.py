#!/usr/bin/python3
"""File Storage Class"""


import json
from models.base_model import BaseModel


class FileStorage:
    """
    This class provides a file storage module for serializing instances
    to a JSON file and deserializing JSON files to instances.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the dictionary of all objects.

        Returns:
            dict: A dictionary containing all objects.
        """
        return self.__objects

    def new(self, obj):
        """
        Adds a new object to the dictionary of objects.

        Args:
            obj: The object to be added.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        Serializes the objects dictionary to a JSON file.
        The JSON file path is specified by __file_path.
        """
        obj_dict = {}
        for key, obj in self.__objects.items():
            obj_dict[key] = obj.to_dict()
        with open(self.__file_path, "w") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserializes the JSON file and updates the objects dictionary.
        If the JSON file (__file_path) exists, it reads file and loads objects
        If the file doesn't exist, it does nothing.
        """
        try:
            with open(self.__file_path, "r") as file:
                obj_dict = json.load(file)
                for key, value in obj_dict.items():
                    class_name, obj_id = key.split(".")
                    self.__objects[key] = globals()[class_name](**value)
        except FileNotFoundError:
            pass
