#!/usr/bin/python3

"""Defines the HBnB console"""

import cmd
import models
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
"""entry point for hbnb console"""


class HBNBCommand(cmd.Cmd):
    """ hbnb shell """
    prompt = '(hbnb) '
    clslist = {'BaseModel': BaseModel, 'State': State, 'City': City,
               'Amenity': Amenity, 'Place': Place, 'Review': Review,
               'User': User}
    def emptyline(self):
        """
        Do nothing when an empty line is entered.
        """
        pass

    def do_create(self, clsname=None):
        """Creates a new instance of BaseModel, saves it and prints the id
        """
        if not clsname:
            print('** class name missing **')
        elif not self.clslist.get(clsname):
            print('** class doesn\'t exist **')
        else:
            obj = self.clslist[clsname]()
            obj.save()
            print(obj.id)

    def do_show(self, arg):
        """Show instance based on id"""
        clsname, objid = None, None
        args = arg.split(' ')
        if len(args) > 0:
            clsname = args[0]
        if len(args) > 1:
            objid = args[1]
        if not clsname:
            print('** class name missing **')
        elif not objid:
            print('** instance id missing **')
        elif not self.clslist.get(clsname):
            print("** class doesn't exist **")
        else:
            k = clsname + "." + objid
            obj = models.storage.all().get(k)
            if not obj:
                print('** no instance found **')
            else:
                print(obj)

    def do_destroy(self, arg):
        """destroy instance based on id"""
        clsname, objid = None, None
        args = arg.split(' ')
        if len(args) > 0:
            clsname = args[0]
        if len(args) > 1:
            objid = args[1]
        if not clsname:
            print('** class name missing **')
        elif not objid:
            print('** instance id missing **')
        elif not self.clslist.get(clsname):
            print("** class doesn't exist **")
        else:
            k = clsname + "." + objid
            obj = models.storage.all().get(k)
            if not obj:
                print('** no instance found **')
            else:
                del models.storage.all()[k]
                models.storage.save()

    def do_all(self, arg):
        """
        Prints all instances or instances of a specific class.
        """
        if arg:
            words = arg.split(' ')
            if words[0] not in models.storage.classes():
                print("** class doesn't exist **")
            else:
                instance_list = [str(obj) for key, obj in models.storage.all().items()
                                if type(obj).__name__ == words[0]]
                print(instance_list)
        else:
            all_instances = [str(obj) for key, obj in models.storage.all().items()]
            print(all_instances)

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        from datetime import datetime
        clsname, objid, attrname, attrval = None, None, None, None
        updatetime = datetime.now()
        args = arg.split(' ')
        if len(args) > 0:
            clsname = args[0]
        if len(args) > 1:
            objid = args[1]
        if len(args) > 2:
            attrname = args[2]
        if len(args) > 3:
            attrval = args[3]
        if not clsname:
            print('** class name missing **')
        elif not objid:
            print('** instance id missing **')
        elif not attrname:
            print('** attribute name missing **')
        elif not attrval:
            print('** value missing **')
        elif not self.clslist.get(clsname):
            print("** class doesn't exist **")
        else:
            k = clsname + "." + objid
            obj = models.storage.all().get(k)
            if not obj:
                print('** no instance found **')
            else:
                obj.__setattr__(attrname,
                                type(obj.__getattribute__(attrname))(attrval))
                obj.updated_at = updatetime
    def do_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """EOF to exit the program
        """
        print()
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
