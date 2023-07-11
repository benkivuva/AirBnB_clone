#!/usr/bin/python3
""" init models """

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()