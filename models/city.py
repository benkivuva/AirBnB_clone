#!/usr/bin/python3
"""Defines the city class"""


from models.base_model import BaseModel


class City(BaseModel):
    """
    child class of BaseModel
    has 2 attributes - state id and name of the city
    """
    state_id = ""
    name = ""
