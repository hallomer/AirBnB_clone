#!/usr/bin/python3
"""file storage class - serialization and deserialization"""
import json


class FileStorage:
    """serializes instances to a JSON file and vice versa"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file"""
        obj_dict = {
            obj_key: obj.to_dict()
            for obj_key, obj in FileStorage.__objects.items()
        }
        with open(FileStorage.__file_path, "w") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        try:
            with open(FileStorage.__file_path, "r") as f:
                obj_dict = json.load(f)
                for obj_key, obj_dict in obj_dict.items():
                    cls_name = obj_dict["__class__"]
                    cls = eval(cls_name)
                    FileStorage.__objects[obj_key] = cls(**obj_dict)
        except FileNotFoundError:
            pass
