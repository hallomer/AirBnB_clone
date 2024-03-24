#!/usr/bin/python3
"""Initialization of models"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
