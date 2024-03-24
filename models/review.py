#!/usr/bin/python3
"""Review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """represents a review"""
    place_id = ""
    user_id = ""
    text = ""
