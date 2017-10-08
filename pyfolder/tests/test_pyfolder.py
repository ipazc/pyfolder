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
import os
import shutil
import unittest

from pyfolder import PyFolder

__author__ = 'Iván de Paz Centeno'


class TestPyFolder(unittest.TestCase):
    """
    Unitary tests for the PyFolder class.
    """
    def setUp(self):
        self.folder = "examples"
        self.test_folders = os.path.join(self.folder, "subdir")

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def test_pyfolder_create_folders(self):
        pyfolder = PyFolder(self.test_folders, auto_create_folder=False)
        self.assertFalse(os.path.exists(self.test_folders))

        # Can't create elements if flag is unset and folder doesn't exist
        with self.assertRaises(FileNotFoundError):
            pyfolder["example"] = "hi"

        pyfolder = PyFolder(self.test_folders, auto_create_folder=True)
        # It must have created the folder
        self.assertTrue(os.path.exists(self.test_folders))

        pyfolder = PyFolder(os.path.join(self.test_folders, "example2", "example3"))

        # It must have created the deep folder
        self.assertTrue(os.path.exists(os.path.join(self.test_folders, "example2", "example3")))

    def test_pyfolder_creates_elements(self):
        """
        PyFolder is able to create elements interpreted/not interpreted
        :return:
        """
        pyfolder = PyFolder(self.test_folders)
        pyfolder["example"] = b"hi"
        self.assertTrue(os.path.exists(os.path.join(self.test_folders, "example")))

        with open(os.path.join(self.test_folders, "example"), "rb") as f:
            content = f.read()
        self.assertEqual(content, b"hi")

        pyfolder["example.txt"] = "hi"
        self.assertTrue(os.path.exists(os.path.join(self.test_folders, "example.txt")))

        with open(os.path.join(self.test_folders, "example.txt"), "r") as f:
            content = f.read()
        self.assertEqual(content, "hi")

        pyfolder["example.json"] = {"m": "hi"}
        self.assertTrue(os.path.exists(os.path.join(self.test_folders, "example.json")))

        with open(os.path.join(self.test_folders, "example.json"), "r") as f:
            content = json.load(f)
        self.assertEqual(content, {"m":"hi"})

        # Disable interpret
        pyfolder = PyFolder(self.test_folders, interpret=False)
        with self.assertRaises(Exception):
            pyfolder["example2.txt"] = {"m":"hi"}

        pyfolder = PyFolder(self.test_folders, interpret=True)
        subdir="subdir/subdir2/file.txt"

        pyfolder[subdir] = "HELLO"

        with open(os.path.join(self.test_folders, subdir), "r") as f:
            content = f.read()
        self.assertEqual(content, "HELLO")

    def test_pyfolder_retrieves_elements(self):
        """
        PyFolder accepts retrieval of elements
        :return:
        """

        pyfolder = PyFolder(self.test_folders)
        with open(os.path.join(self.test_folders, "example"), "wb") as f:
            f.write(b"hi")

        self.assertEqual(pyfolder["example"],  b"hi")

        with open(os.path.join(self.test_folders, "example.txt"), "w") as f:
            f.write("hi")

        self.assertEqual(pyfolder["example.txt"],  "hi")

        with open(os.path.join(self.test_folders, "example.json"), "w") as f:
            json.dump({"m":"h"}, f)

        self.assertEqual(pyfolder["example.json"],  {"m":"h"})

        with self.assertRaises(KeyError):
            a = pyfolder["UNKNOWN"]

    def test_pyfolder_deletes_elements(self):
        """
        PyFolder accepts delete of elements
        :return:
        """
        pyfolder = PyFolder(self.test_folders)

        pyfolder["prueba"] = b"hola"
        pyfolder["test/example.txt"] = "jeje"

        with self.assertRaises(Exception):
            del pyfolder["."]
            del pyfolder["prueba"]
            del pyfolder["test/example.txt"]
            del pyfolder["test"]

        pyfolder = PyFolder(self.test_folders, allow_remove_folders_with_content=True)

        with self.assertRaises(Exception):
            del pyfolder["."]
            del pyfolder["test"]
            del pyfolder["test/example.txt"]

        pyfolder = PyFolder(self.test_folders, allow_override=True)

        with self.assertRaises(OSError):
            del pyfolder["test"]
            del pyfolder["."]

        pyfolder2 = PyFolder(os.path.join(self.test_folders, "example"), allow_override=True)
        self.assertTrue(os.path.exists(os.path.join(self.test_folders, "example")))
        del pyfolder["example"]
        self.assertFalse(os.path.exists(os.path.join(self.test_folders, "example")))

        self.assertTrue(os.path.exists(os.path.join(self.test_folders, "prueba")))
        del pyfolder["prueba"]
        self.assertFalse(os.path.exists(os.path.join(self.test_folders, "prueba")))

        pyfolder = PyFolder(self.test_folders, allow_override=True, allow_remove_folders_with_content=True)

        self.assertTrue(os.path.exists(os.path.join(self.test_folders, "test")))
        del pyfolder["test"]
        self.assertFalse(os.path.exists(os.path.join(self.test_folders, "test")))

        self.assertTrue(os.path.exists(self.test_folders))
        del pyfolder["."]
        self.assertFalse(os.path.exists(self.test_folders))

    def test_pyfolder_edits_elements(self):
        """
        PyFolder accepts edit of elements
        :return:
        """

        pyfolder = PyFolder(self.test_folders)

        pyfolder["foo"] = b"bar"

        with self.assertRaises(Exception):
            pyfolder["foo"] = b"foo"

        pyfolder = PyFolder(self.test_folders, allow_override=True)
        pyfolder["foo"] = b"foo"
        self.assertEqual(pyfolder["foo"], b"foo")

    def test_pyfolder_contains_elements(self):
        """
        PyFolder accepts the "in" keyword to lookup for elements
        :return:
        """

        pyfolder = PyFolder(self.test_folders)

        pyfolder["foo"] = b"bar"
        pyfolder["foo2"] = b"bar2"

        self.assertIn("foo", pyfolder)
        self.assertIn("foo2", pyfolder)
        self.assertNotIn("foo3", pyfolder)

    def test_pyfolder_keys(self):
        """
        PyFolder is able to return its keys
        :return:
        """
        pyfolder = PyFolder(self.test_folders)

        pyfolder["foo"] = b"bar"
        pyfolder["foo2"] = b"bar2"

        self.assertTrue(all(x in pyfolder.keys() for x in ["foo", "foo2"]))
        self.assertEqual(len(pyfolder.keys()), 2)

    def test_pyfolder_values(self):
        """
        PyFolder successfully returns the values o its keys
        :return:
        """
        pyfolder = PyFolder(self.test_folders)

        pyfolder["foo"] = b"bar"
        pyfolder["foo2"] = b"bar2"

        self.assertTrue(all(x in pyfolder.values() for x in [b"bar", b"bar2"]))
        self.assertEqual(len(pyfolder.values()), 2)

    def test_pyfolder_iterate(self):
        """
        PyFolder can be iterated
        :return:
        """
        pyfolder = PyFolder(self.test_folders)

        pyfolder["foo"] = b"bar"
        pyfolder["foo2"] = b"bar2"

        for element in pyfolder:
            self.assertTrue(element in ["foo", "foo2"])

        for element, content in pyfolder.items():
            self.assertEqual(content, {"foo": b"bar", "foo2": b"bar2"}[element])

        pyfolder["foo3/foo"] = b"bar"

        for element in pyfolder:
            self.assertTrue(element in ["foo", "foo2", "foo3"])

        for element, content in pyfolder.items():
            if element == "foo3":
                self.assertTrue(type(content) is PyFolder)

    def test_pyfolder_iterate_only_files(self):
        """
        PyFolder is able to iterate only over files
        :return:
        """
        pyfolder = PyFolder(self.test_folders)

        pyfolder["foo"] = b"bar"
        pyfolder["foo2"] = b"bar2"
        pyfolder["foo3/foo"] = b"bar"

        for element in pyfolder.files():
            self.assertTrue(element in ["foo", "foo2"])

        for element, content in pyfolder.files_items():
            self.assertEqual(content, {"foo": b"bar", "foo2": b"bar2"}[element])

    def test_pyfolder_iterate_only_folders(self):
        """
        PyFolder is able to iterate only over folders.
        :return:
        """
        pyfolder = PyFolder(self.test_folders)

        pyfolder["foo"] = b"bar"
        pyfolder["foo2"] = b"bar2"
        pyfolder["foo3/foo"] = b"bar"

        for element in pyfolder.folders():
            self.assertTrue(element in ["foo3"])

        for element, content in pyfolder.folders_items():
            self.assertTrue(type(content) is PyFolder)
            self.assertIn("foo", content)

    def test_pyfolder_index(self):
        """
        PyFolder is able to find elements
        :return:
        """
        pyfolder = PyFolder(self.test_folders)

        pyfolder["foo"] = b"bar"
        pyfolder["foo2"] = b"bar2"
        pyfolder["foo3/foo"] = b"bar"

        indexes = pyfolder.index("foo")
        self.assertEqual(len(indexes), 2)
        self.assertIn("foo", indexes)
        self.assertIn("foo3/foo", indexes)

if __name__ == '__main__':
    unittest.main()