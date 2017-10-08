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

import os
import shutil

from pyfolder.interpreters import Interpreters, BinaryInterpreter, JSONInterpreter, TextInterpreter

__author__ = "Iván de Paz Centeno"

class PyFolder(dict):

    def __init__(self, folder_root, auto_create_folder=True, interpret=True, allow_override=False,
                 allow_remove_folders_with_content=False, interpreters=None):

        self.folder_root = folder_root
        self.auto_create_folder = auto_create_folder
        self.interpret = interpret
        self.allow_override = allow_override
        self.allow_remove_folders_with_content = allow_remove_folders_with_content

        if interpreters is None:
            interpreters = Interpreters()

            if interpret:
                interpreters.register(JSONInterpreter())
                interpreters.register(TextInterpreter())

            interpreters.register(BinaryInterpreter())

        self.interpreters = interpreters

        if auto_create_folder:
            os.makedirs(folder_root, exist_ok=True)

    def __str__(self):
        return "{} ({} elements)".format(self.folder_root, len(self))

    def __len__(self):
        return len(os.listdir(self.folder_root))

    def __repr__(self):
        return str(self)

    def __iter__(self):
        for file_name in os.listdir(self.folder_root):
            yield file_name

    def keys(self):
        return list(os.listdir(self.folder_root))

    def values(self):
        return [value for _, value in self.items()]

    def __contains__(self, item):
        return item in self.keys()

    def __setitem__(self, key, value):
        if ".." in key or key == ".":
            raise KeyError("Invalid key {}".format(key))

        father, item_name = self.__get_uri_item_name(key)

        if not self.allow_override and item_name in father:
            raise Exception("File {} already exists and can't be overridden (flag not set)".format(
                os.path.join(father.folder_root, item_name)))

        self.interpreters.save(os.path.join(father.folder_root, item_name), value)

    def __getitem__(self, item):
        if ".." in item:
            raise KeyError("Invalid key {}".format(item))

        if item == ".":
            return self

        father, item_name = self.__get_uri_item_name(item)

        if not os.path.exists(os.path.join(father.folder_root, item_name)):
            raise KeyError(item)

        if os.path.isfile(os.path.join(father.folder_root, item_name)):
            content = self.interpreters.load(os.path.join(self.folder_root, item))
        else:
            content = PyFolder(os.path.join(father.folder_root, item_name),
                                  auto_create_folder=self.auto_create_folder, interpret=self.interpret,
                                  allow_override=self.allow_override,
                                  allow_remove_folders_with_content=self.allow_remove_folders_with_content,
                                        interpreters=self.interpreters)
        return content

    def __get_uri_item_name(self, item):
        if "/" in item:
            items = item.split("/")

            iterator = self

            for path in items[:-1]:
                iterator = PyFolder(os.path.join(iterator.folder_root, path),
                                      auto_create_folder=self.auto_create_folder, interpret=self.interpret,
                                      allow_override=self.allow_override,
                                      allow_remove_folders_with_content=self.allow_remove_folders_with_content,
                                        interpreters=self.interpreters)

            result = iterator, items[-1]
        else:
            result = self, item

        return result

    def items(self):
        for file_name in os.listdir(self.folder_root):

            if os.path.isfile(os.path.join(self.folder_root, file_name)):
                content = self.interpreters.load(os.path.join(self.folder_root, file_name))
            else:
                content = PyFolder(os.path.join(self.folder_root, file_name),
                                      auto_create_folder=self.auto_create_folder, interpret=self.interpret,
                                      allow_override=self.allow_override,
                                      allow_remove_folders_with_content=self.allow_remove_folders_with_content,
                                        interpreters=self.interpreters)

            yield file_name, content

    def files(self):
        for file_name in os.listdir(self.folder_root):
            if os.path.isfile(os.path.join(self.folder_root, file_name)):
                yield file_name

    def folders(self):
        for folder in os.listdir(self.folder_root):
            if os.path.isfile(os.path.join(self.folder_root, folder)):
                continue
            yield folder

    def files_items(self):
        for file_name in self.files():
            content = self.interpreters.load(os.path.join(self.folder_root, file_name))
            yield file_name, content

    def folders_items(self):
        for folder_name in self.folders():
            yield folder_name, PyFolder(os.path.join(self.folder_root, folder_name),
                                      auto_create_folder=self.auto_create_folder, interpret=self.interpret,
                                      allow_override=self.allow_override,
                                      allow_remove_folders_with_content=self.allow_remove_folders_with_content,
                                        interpreters=self.interpreters)

    def __delitem__(self, key):
        if ".." in key:
            raise KeyError("Invalid key {}".format(key))

        if not self.allow_override:
            raise Exception("File {} can't be deleted (flag not set)".format(
                os.path.join(self.folder_root, key)))

        if key == ".":
            self.__delete(self.allow_remove_folders_with_content)
            return

        father, item_name = self.__get_uri_item_name(key)

        if os.path.isfile(os.path.join(father.folder_root, item_name)):
            os.remove(os.path.join(father.folder_root, item_name))
        else:
            father[item_name].__delete(self.allow_remove_folders_with_content)

    def __delete(self, force=False):
        if force:
            shutil.rmtree(self.folder_root, ignore_errors=True)
        else:
            os.rmdir(self.folder_root)

    def index(self, filename, max_depth=200):
        matches = self.__index(filename, max_depth)
        folder_root = self.folder_root
        if not folder_root.endswith("/"): folder_root += "/"

        return [match.replace(folder_root, "") for match in matches]

    def __index(self, filename, max_depth):
        matches = []

        if max_depth == 0:
            return matches

        for f in self.files():
            if f == filename:
                matches.append(os.path.join(self.folder_root, f))

        for f, folder in self.folders_items():
            if f == filename:
                matches.append(os.path.join(self.folder_root, f))
            matches += folder.__index(filename, max_depth-1)

        return matches
