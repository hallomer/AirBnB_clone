#!/usr/bin/python3
"""cmd class for console"""
import cmd
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """cmd class for console"""
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program"""
        print("")
        return True

    def emptyline(self):
        """does nothing on empty line input"""
        pass

    def do_create(self, arg):
        """creates a new instance of the specified class"""
        if not arg:
            print("** class name missing **")
        elif arg not in ["BaseModel", "User", "State",
                         "City", "Amenity", "Place", "Review"]:
            print("** class doesn't exist **")
        else:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """prints the string representation of an instance"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in ["BaseModel", "User", "State",
                             "City", "Amenity", "Place", "Review"]:
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
        """deletes an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in ["BaseModel", "User", "State",
                             "City", "Amenity", "Place", "Review"]:
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
        """prints all string representations of all instances of a class"""
        args = arg.split()
        if not args:
            print([str(obj) for obj in storage.all().values()])
        elif args[0] not in ["BaseModel", "User", "State",
                             "City", "Amenity", "Place", "Review"]:
            print("** class doesn't exist **")
        else:
            print([str(obj) for key, obj
                   in storage.all().items() if key.startswith(args[0])])

    def do_update(self, arg):
        """updates an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in ["BaseModel", "User", "State",
                             "City", "Amenity", "Place", "Review"]:
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
