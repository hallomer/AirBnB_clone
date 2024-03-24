#!/usr/bin/python3
"""
Module for the HBNBCommand class
"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models import storage


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the HBNB project"""
    prompt = "(hbnb) "
    classes = {"BaseModel": BaseModel, "User": User}

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program"""
        print("")
        return True

    def emptyline(self):
        """Does nothing on empty line input"""
        pass

    def do_create(self, arg):
        """
        Creates a new instance of the specified class
        Usage: create <class_name>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            new_instance = HBNBCommand.classes[args[0]]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        Usage: show <class_name> <instance_id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[key])

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        Usage: destroy <class_name> <instance_id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, arg):
        """
        Prints all string representations of all instances of a class
        Usage: all <optional_class_name>
        """
        args = arg.split()
        instances = []
        if not args:
            instances = [str(obj) for obj in storage.all().values()]
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            instances = [str(obj) for key, obj in storage.all().items()
                         if key.startswith(args[0])]
        print(instances)

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id
        Usage: update <class_name> <instance_id> <attribute_name> <attribute_value>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            elif len(args) < 3:
                print("** attribute name missing **")
            elif len(args) < 4:
                print("** value missing **")
            else:
                setattr(storage.all()[key], args[2], args[3])
                storage.all()[key].save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()