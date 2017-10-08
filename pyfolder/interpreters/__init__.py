#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#MIT License
#
#Copyright (c) 2017 Iván de Paz Centeno
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

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

        loaded = False
        result = b""

        for interpreter in self.interpreter_list:
            if interpreter.can_load(extension):
                error = None
                try:
                    result = interpreter.load(uri)
                    loaded = True

                except Exception as ex:
                    error = str(ex)

                if error:
                    raise Exception("Error loading file \"{}\": {}".format(uri, error))

                break

        if not loaded:
            raise FileNotFoundError(uri)

        return result

    def save(self, uri, object):
        saved = False

        for interpreter in self.interpreter_list:
            if interpreter.can_save(object):
                error = None
                try:
                    result = interpreter.save(uri, object)
                    saved = True
                except Exception as ex:
                    error = str(ex)

                if error:
                    raise Exception("Error saving file \"{}\": {}".format(uri, error))

                break

        if not saved:
            raise Exception("Can't save the object \"{}\": {}".format(object, "Unknown type"))


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
