#!/usr/bin/python3
"""User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """represents a user"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
