#!/usr/bin/python3
"""Defines the BaseModel"""


from uuid import uuid4
from datetime import datetime


class BaseModel:
    """The super class"""
    def __init__(self):
        """Initializing the base model"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def __str__(self):
        """sets the print behaviour of the base model"""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """updates up_dated with current datetime"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """returns a dictionary containing all key/values of __dict__"""
        new_dict = self.__dict__.copy()
        new_dict["created_at"] = self.created_at.isoformat
        new_dict["updated_at"] = self.updated_at.isoformat
        new_dict["__class__"] = self.__class__.__name__
        return new_dict
