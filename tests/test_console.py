#!/usr/bin/python3
"""
Unittest for the HBNBCommand class (console)
"""
import unittest
from io import StringIO
import sys
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User


class TestHBNBCommand(unittest.TestCase):
    """Unit tests for the HBNBCommand class"""

    def setUp(self):
        """Redirect stdout to capture command output"""
        self.console = HBNBCommand()
        self.output = StringIO()
        sys.stdout = self.output

    def tearDown(self):
        """Restore stdout after each test"""
        self.output.close()
        sys.stdout = sys.__stdout__

    def test_create_missing_class(self):
        """Test create command with no class name"""
        self.console.onecmd("create")
        self.assertIn("** class name missing **", self.output.getvalue().strip())

    def test_create_invalid_class(self):
        """Test create command with an invalid class name"""
        self.console.onecmd("create InvalidClass")
        self.assertIn("** class doesn't exist **", self.output.getvalue().strip())

    def test_create_valid_class(self):
        """Test create command with a valid class name"""
        self.console.onecmd("create BaseModel")
        output = self.output.getvalue().strip()
        key = f"BaseModel.{output}"
        self.assertIn(key, storage.all().keys())

    def test_show_missing_class(self):
        """Test show command with missing class name"""
        self.console.onecmd("show")
        self.assertIn("** class name missing **", self.output.getvalue().strip())

    def test_show_missing_id(self):
        """Test show command with missing instance id"""
        self.console.onecmd("show BaseModel")
        self.assertIn("** instance id missing **", self.output.getvalue().strip())

    def test_show_no_instance_found(self):
        """Test show command with a non-existent instance id"""
        self.console.onecmd("show BaseModel 1234")
        self.assertIn("** no instance found **", self.output.getvalue().strip())

    def test_destroy_missing_class(self):
        """Test destroy command with missing class name"""
        self.console.onecmd("destroy")
        self.assertIn("** class name missing **", self.output.getvalue().strip())

    def test_destroy_missing_id(self):
        """Test destroy command with missing instance id"""
        self.console.onecmd("destroy BaseModel")
        self.assertIn("** instance id missing **", self.output.getvalue().strip())

    def test_destroy_no_instance_found(self):
        """Test destroy command with a non-existent instance id"""
        self.console.onecmd("destroy BaseModel 1234")
        self.assertIn("** no instance found **", self.output.getvalue().strip())

    def test_all_command(self):
        """Test all command to list all instances"""
        self.console.onecmd("all")
        output = self.output.getvalue().strip()
        self.assertIsInstance(output, str)

    def test_all_class_command(self):
        """Test all command with a specific class"""
        self.console.onecmd("all BaseModel")
        output = self.output.getvalue().strip()
        self.assertIsInstance(output, str)

    def test_update_missing_class(self):
        """Test update command with missing class name"""
        self.console.onecmd("update")
        self.assertIn("** class name missing **", self.output.getvalue().strip())

    def test_update_missing_id(self):
        """Test update command with missing instance id"""
        self.console.onecmd("update BaseModel")
        self.assertIn("** instance id missing **", self.output.getvalue().strip())

    def test_update_no_instance_found(self):
        """Test update command with a non-existent instance id"""
        self.console.onecmd("update BaseModel 1234")
        self.assertIn("** no instance found **", self.output.getvalue().strip())

    def test_update_add_attribute(self):
        """Test update command with adding a new attribute"""
        self.console.onecmd("create User")
        user_id = self.output.getvalue().strip()
        self.output.truncate(0)
        self.output.seek(0)

        self.console.onecmd(f"update User {user_id} name 'John'")
        self.console.onecmd(f"show User {user_id}")
        output = self.output.getvalue().strip()
        self.assertIn("'name': \"'John'\"", output)


if __name__ == "__main__":
    unittest.main()

