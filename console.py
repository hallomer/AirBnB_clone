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
    classes = {"BaseModel": BaseModel, "User": User, "Place": Place,
               "State": State, "City": City,
               "Amenity": Amenity, "Review": Review}

    def help_help(self):
        """Help documentation for help method"""
        output = """Help:
    how to use
        create  Usage: create <class name>
        show    Usage: show <class name> <ID>
        destroy Usage: destroy <class name> <ID>
        all     Usage: all <class name > || all
        update  Usage: update <class name> <ID>\
            <attribute name> <attribute value>
        count   Usage: count <class_name>"""
        print(output)
        return

    def help_quit(self):
        """Help documentation for quit method"""
        print("Quit the command interpreter\n")

    def help_EOF(self):
        """Help documentation for EOF method"""
        print("EOF Quit the command interpreter\n")

    def help_create(self):
        """Help documentation for create method"""
        print("Usage: create <class name>")
        return

    def help_show(self):
        """Help documentation for show method"""
        print("Usage: show <class name> <ID>")
        return

    def help_destroy(self):
        """Help documentation for destroy method"""
        print("Usage: destroy <class name> <ID>")
        return

    def help_all(self):
        """Help documentation for all method"""
        print("all <class name > || all")

    def help_update(self):
        """Help documentation for update method"""
        print("Usage: update <class name> <id> \
              <attribute name> \"<attribute value>\"")

    def help_count(self):
        """Help documentation for count method"""
        print("Usage: count <class_name>")

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
        Usage:update<class_name><instance_id><attribute_name><attribute_value>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif len(args) < 3:
            print("** attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                setattr(storage.all()[key], args[2], args[3])
                storage.all()[key].save()

    def default(self, line):
        """Handles default behavior for unrecognized commands"""
        command_parts = line.split(".")
        if len(command_parts) == 2:
            class_name = command_parts[0]
            if class_name in HBNBCommand.classes:
                command = command_parts[1].split("(")[0]
                if command == "all":
                    class_name = command_parts[0]
                    command = "all {}".format(class_name)
                    self.onecmd(command)
                    return
                elif command == "show":
                    args = command_parts[1]\
                        .split("(")[1].split(")")[0].split(",")
                    instance_id = args[0].strip(' \'"')
                    command = "show {} {}".format(class_name, instance_id)
                    self.onecmd(command)
                    return
                elif command == "destroy":
                    args = command_parts[1]\
                        .split("(")[1].split(")")[0].split(",")
                    instance_id = args[0].strip(' \'"')
                    command = "destroy {} {}".format(class_name, instance_id)
                    self.onecmd(command)
                    return
                elif command == "update":
                    args = command_parts[1]\
                        .split("(")[1].split(")")[0].split(",")
                    instance_id = args[0].strip(' \'"')
                    attribute_name = args[1].strip(' \'"')
                    attribute_value = args[2].strip(' \'"')
                    command = f"update {class_name} {instance_id}\
                        {attribute_name} {attribute_value}"
                    self.onecmd(command)
                    return
                elif command == "count":
                    command = "count {}".format(class_name)
                    self.onecmd(command)
                    return
        print("*** Unknown syntax: {}".format(line))

    def do_count(self, arg):
        """
        Counts the number of instances of a class
        Usage: count <class_name>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            class_name = args[0]
            count = 0
            for key in storage.all():
                if key.split('.')[0] == class_name:
                    count += 1
            print(count)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
