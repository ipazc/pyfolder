#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

__author__ = "Iván de Paz Centeno"

class Interpreter(object):

    def can_load(self, extension):
        """
        Checks if the extension matches this interpreter.
        :param extension: Extension string (may or not include the initial ".")
        :return: True if matches (can be loaded), False otherwise.
        """
        pass

    def can_save(self, object):
        """
        Checks if this interpreter can manage this object to store into a file.
        :param object: Object to check for store.
        :return: True if matches (can be saved), False otherwise.
        """
        pass

    def load(self, uri):
        """
        Loads a file
        :param uri: relative URI to the file
        :return: content of the file interpreted.
        """
        pass

    def save(self, uri, object):
        """
        Saves the object into the file.
        :param uri: path to store the object.
        :param object: object to save
        """
        pass


class Interpreters(object):

    def __init__(self):
        self.interpreter_list = []

    def register(self, interpreter):
        self.interpreter_list.append(interpreter)

    def load(self, uri):
        try:
            extension = uri.split(".")[1]
        except IndexError as ex:
            extension = ""

        result = b""

        for interpreter in self.interpreter_list:
            if interpreter.can_load(extension):
                error = None
                try:
                    result = interpreter.load(uri)
                except Exception as ex:
                    error = str(ex)

                if error:
                    raise Exception("Error loading file \"{}\": {}".format(uri, error))

                break

        return result

    def save(self, uri, object):
        for interpreter in self.interpreter_list:
            if interpreter.can_save(object):
                error = None
                try:
                    result = interpreter.save(uri, object)
                except Exception as ex:
                    error = str(ex)

                if error:
                    raise Exception("Error saving file \"{}\": {}".format(uri, error))

                break


class BinaryInterpreter(Interpreter):
    def can_load(self, extension):
        # The binary interpreter matches any extension
        return True

    def can_save(self, object):
        # The binary interpreter can only save bytes objects
        return type(object) is bytes

    def load(self, uri):
        with open(uri, "rb") as f:
            content = f.read()
        return content

    def save(self, uri, object):
        with open(uri, "wb") as f:
            f.write(object)


class JSONInterpreter(Interpreter):
    def can_load(self, extension):
        return extension.lower().endswith("json")

    def can_save(self, object):
        return type(object) is dict or type(object) is list

    def load(self, uri):
        with open(uri, "r") as f:
            content = json.load(f)
        return content

    def save(self, uri, object):
        with open(uri, "w") as f:
            json.dump(object, f, indent=4)


class TextInterpreter(Interpreter):
    def __init__(self):
        self.extensions = ["txt", "csv", "conf", "ini"]

    def can_load(self, extension):
        return any([extension.lower().endswith(e) for e in self.extensions])

    def can_save(self, object):
        # The binary interpreter can only save bytes objects
        return type(object) is str

    def load(self, uri):
        with open(uri, "r") as f:
            content = f.read()
        return content

    def save(self, uri, object):
        with open(uri, "w") as f:
            f.write(object)
