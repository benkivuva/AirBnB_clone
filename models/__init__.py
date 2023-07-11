#!/usr/bin/python3
""" init the models """

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
