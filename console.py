#!/usr/bin/python3

"""Defines the HBnB console"""

import cmd
import json
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """ hbnb shell """
    prompt = '(hbnb) '
    clslist = {'BaseModel': BaseModel}

    def do_quit(self, arg):
        """
        Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """
        EOF command to exit the program
        """
        return True

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
            k = clsname + "." + objid;
            obj = models.storage.all().get(k)
            if not obj:
                print('** no instance found **')
            else:
                print(obj)


    if __name__ == "__main__":
     HBNBCommand().cmdloop()     