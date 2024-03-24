#!/usr/bin/python3
"""
Module for Amenity class unittest
"""
import unittest
from unittest.mock import patch
from io import StringIO
from models import storage
from console import HBNBCommand


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

    def test_do_all(self):
        """Test the do_all method"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.do_all('')
        output = f.getvalue().strip()
        self.assertEqual(output, '[]')

    def test_do_update(self):
        """Test the do_update method"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.do_update('BaseModel 123 name "John"')
        output = f.getvalue().strip()
        self.assertEqual(output, '** no instance found **')

    def test_default(self):
        """Test the default method"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.default('BaseModel.all()')
        output = f.getvalue().strip()
        self.assertEqual(output, '[]')

    def test_do_count(self):
        """Test the do_count method"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.do_count('BaseModel')
        output = f.getvalue().strip()
        self.assertEqual(output, '0')


if __name__ == '__main__':
    unittest.main()
