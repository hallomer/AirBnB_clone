#!/usr/bin/python3
"""
Module for Amenity class unittest
"""
import unittest
from unittest.mock import patch
from io import StringIO
from models import storage
from console import HBNBCommand
from models.engine.file_storage import FileStorage
import os


class TestHBNBCommand(unittest.TestCase):
    """
    Test cases for the HBNBCommand class
    """

    def setUp(self):
        self.cli = HBNBCommand()

    def test_help_help(self):
        """Test the help_help method"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.help_help()
            output = f.getvalue()
        expected_output = """Help:
    how to use
        create  Usage: create <class name>
        show    Usage: show <class name> <ID>
        destroy Usage: destroy <class name> <ID>
        all     Usage: all <class name > || all
        update  Usage: update <class name> <ID>\
            <attribute name> <attribute value>
        count   Usage: count <class_name>"""
        self.assertEqual(output.strip(), expected_output.strip())

    def test_do_quit(self):
        """Test the do_quit method"""
        with patch('sys.stdout', new=StringIO()) as f:
            result = self.cli.do_quit(None)
        self.assertTrue(result)

    def test_do_EOF(self):
        """Test the do_EOF method"""
        with patch('sys.stdout', new=StringIO()) as f:
            result = self.cli.do_EOF(None)
        self.assertTrue(result)

    def test_emptyline(self):
        """Test the emptyline method"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.emptyline()
        output = f.getvalue()
        self.assertEqual(output, '')

    def test_do_create(self):
        """Test the do_create method"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.do_create('BaseModel')
        output = f.getvalue().strip()
        self.assertRegex(output, r'^[\w-]+$')

    def test_do_show(self):
        """Test the do_show method"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.do_show('BaseModel 123')
        output = f.getvalue().strip()
        self.assertEqual(output, '** no instance found **')

    def test_do_destroy(self):
        """Test the do_destroy method"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.do_destroy('BaseModel 123')
        output = f.getvalue().strip()
        self.assertEqual(output, '** no instance found **')

    def test_do_update(self):
        """Test the do_update method"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.do_update('BaseModel 123 name "John"')
        output = f.getvalue().strip()
        self.assertEqual(output, '** no instance found **')

    class TestHBNBCommand_all(unittest.TestCase):
        """Unittests for testing all of the HBNB command interpreter."""

        @classmethod
        def setUp(self):
            try:
                os.rename("file.json", "tmp")
            except IOError:
                pass
            FileStorage.__objects = {}

        @classmethod
        def tearDown(self):
            try:
                os.remove("file.json")
            except IOError:
                pass
            try:
                os.rename("tmp", "file.json")
            except IOError:
                pass

        def test_all_invalid_class(self):
            correct = "** class doesn't exist **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all MyModel"))
                self.assertEqual(correct, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
                self.assertEqual(correct, output.getvalue().strip())

        def test_all_objects_space_notation(self):
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
                self.assertFalse(HBNBCommand().onecmd("create User"))
                self.assertFalse(HBNBCommand().onecmd("create State"))
                self.assertFalse(HBNBCommand().onecmd("create Place"))
                self.assertFalse(HBNBCommand().onecmd("create City"))
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
                self.assertFalse(HBNBCommand().onecmd("create Review"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all"))
                self.assertIn("BaseModel", output.getvalue().strip())
                self.assertIn("User", output.getvalue().strip())
                self.assertIn("State", output.getvalue().strip())
                self.assertIn("Place", output.getvalue().strip())
                self.assertIn("City", output.getvalue().strip())
                self.assertIn("Amenity", output.getvalue().strip())
                self.assertIn("Review", output.getvalue().strip())

        def test_all_objects_dot_notation(self):
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
                self.assertFalse(HBNBCommand().onecmd("create User"))
                self.assertFalse(HBNBCommand().onecmd("create State"))
                self.assertFalse(HBNBCommand().onecmd("create Place"))
                self.assertFalse(HBNBCommand().onecmd("create City"))
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
                self.assertFalse(HBNBCommand().onecmd("create Review"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(".all()"))
                self.assertIn("BaseModel", output.getvalue().strip())
                self.assertIn("User", output.getvalue().strip())
                self.assertIn("State", output.getvalue().strip())
                self.assertIn("Place", output.getvalue().strip())
                self.assertIn("City", output.getvalue().strip())
                self.assertIn("Amenity", output.getvalue().strip())
                self.assertIn("Review", output.getvalue().strip())

        def test_all_single_object_space_notation(self):
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
                self.assertFalse(HBNBCommand().onecmd("create User"))
                self.assertFalse(HBNBCommand().onecmd("create State"))
                self.assertFalse(HBNBCommand().onecmd("create Place"))
                self.assertFalse(HBNBCommand().onecmd("create City"))
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
                self.assertFalse(HBNBCommand().onecmd("create Review"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
                self.assertIn("BaseModel", output.getvalue().strip())
                self.assertNotIn("User", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all User"))
                self.assertIn("User", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all State"))
                self.assertIn("State", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all City"))
                self.assertIn("City", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all Amenity"))
                self.assertIn("Amenity", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all Place"))
                self.assertIn("Place", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all Review"))
                self.assertIn("Review", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())

        def test_all_single_object_dot_notation(self):
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
                self.assertFalse(HBNBCommand().onecmd("create User"))
                self.assertFalse(HBNBCommand().onecmd("create State"))
                self.assertFalse(HBNBCommand().onecmd("create Place"))
                self.assertFalse(HBNBCommand().onecmd("create City"))
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
                self.assertFalse(HBNBCommand().onecmd("create Review"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
                self.assertIn("BaseModel", output.getvalue().strip())
                self.assertNotIn("User", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("User.all()"))
                self.assertIn("User", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("State.all()"))
                self.assertIn("State", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("City.all()"))
                self.assertIn("City", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
                self.assertIn("Amenity", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Place.all()"))
                self.assertIn("Place", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Review.all()"))
                self.assertIn("Review", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())

    class TestHBNBCommand_count(unittest.TestCase):
        """Unittests for testing count method of HBNB comand interpreter."""

        @classmethod
        def setUp(self):
            try:
                os.rename("file.json", "tmp")
            except IOError:
                pass
            FileStorage._FileStorage__objects = {}

        @classmethod
        def tearDown(self):
            try:
                os.remove("file.json")
            except IOError:
                pass
            try:
                os.rename("tmp", "file.json")
            except IOError:
                pass

        def test_count_invalid_class(self):
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
                self.assertEqual("0", output.getvalue().strip())

        def test_count_object(self):
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
                self.assertEqual("1", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create User"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("User.count()"))
                self.assertEqual("1", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create State"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("State.count()"))
                self.assertEqual("1", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Place"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Place.count()"))
                self.assertEqual("1", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create City"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("City.count()"))
                self.assertEqual("1", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
                self.assertEqual("1", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Review"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Review.count()"))
                self.assertEqual("1", output.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
