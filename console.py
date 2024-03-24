#!/usr/bin/python3
"""
Module for the HBNBCommand class
"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the HBNB project"""
    prompt = "(hbnb) "
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Review": Review
    }

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
        elif len(args) < 4:
            print("** attribute name and/or value missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                instance = storage.all()[key]
                attribute_name = args[2]
                attribute_value = args[3]
                if hasattr(instance, attribute_name):
                    attribute_value = type(getattr(instance, attribute_name))(attribute_value)
                    setattr(instance, attribute_name, attribute_value)
                    instance.save()
                else:
                    print("** attribute doesn't exist **")



    def default(self, line):
        """Handles default behavior for unrecognized commands"""
        command_parts = line.split(".")
        if len(command_parts) == 2:
            class_and_method = command_parts[1].split("(")
            class_name = command_parts[0]
            method_name = class_and_method[0]
            if class_name in HBNBCommand.classes and len(class_and_method) >= 2:
                instance_id = class_and_method[1].split(",")[0].replace("(", "").replace("'", "").replace('"', '').strip()
                if method_name == "show":
                    command = f"show {class_name} {instance_id}"
                    self.onecmd(command)
                    return
                elif method_name == "destroy":
                    command = f"destroy {class_name} {instance_id}"
                    self.onecmd(command)
                    return
                elif method_name == "update":
                    command_args = class_and_method[1].split(",", maxsplit=1)[1].replace(")", "").strip()
                    try:
                        attributes_dict = eval(command_args)
                        if isinstance(attributes_dict, dict):
                            for attribute_name, attribute_value in attributes_dict.items():
                                attribute_name = attribute_name.strip().replace("'", "").replace('"', '')
                                attribute_value = str(attribute_value).strip().replace("'", "").replace('"', '')
                                command = f"update {class_name} {instance_id} {attribute_name} {attribute_value}"
                                self.onecmd(command)
                            return
                    except (SyntaxError, NameError):
                        pass
        print("*** Unknown syntax: {}".format(line))

if __name__ == "__main__":
    HBNBCommand().cmdloop()