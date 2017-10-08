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
from pyfolder import BinaryInterpreter, JSONInterpreter, TextInterpreter, Interpreters


__author__ = 'Iván de Paz Centeno'


class TestInterpreters(unittest.TestCase):
    """
    Unitary tests for the Interpreters classes.
    """

    def setUp(self):
        self.folder = "examples"
        os.mkdir(self.folder)

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def test_binary_interpreter(self):
        """
        BinaryInterpreter works as expected
        """
        interpreter = BinaryInterpreter()

        content = b"this is a bytes object"

        self.assertTrue(interpreter.can_save(content))
        self.assertFalse(interpreter.can_save("this is not bytes"))

        interpreter.save(os.path.join(self.folder, "example"), content)

        self.assertTrue(interpreter.can_load(""))
        content2 = interpreter.load(os.path.join(self.folder, "example"))
        self.assertEqual(content, content2)

    def test_json_interpreter(self):
        """
        JSONInterpreter works as expected
        """
        interpreter = JSONInterpreter()

        content = {"this": "is a json object"}

        self.assertTrue(interpreter.can_save(content))
        self.assertFalse(interpreter.can_save("this is not json"))
        self.assertFalse(interpreter.can_save(b"nor this"))

        interpreter.save(os.path.join(self.folder, "example.json"), content)

        self.assertFalse(interpreter.can_load("txt"))
        self.assertTrue(interpreter.can_load("json"))
        content2 = interpreter.load(os.path.join(self.folder, "example.json"))
        self.assertEqual(content, content2)

    def test_text_interpreter(self):
        """
        TextInterpreter works as expected
        """
        interpreter = TextInterpreter()

        content = "This is just plain text"

        self.assertTrue(interpreter.can_save(content))
        self.assertFalse(interpreter.can_save(["this is not plain text"]))
        self.assertFalse(interpreter.can_save(b"nor this"))

        interpreter.save(os.path.join(self.folder, "example.txt"), content)

        self.assertTrue(interpreter.can_load("txt"))
        self.assertTrue(interpreter.can_load("csv"))
        self.assertTrue(interpreter.can_load("conf"))
        self.assertTrue(interpreter.can_load("ini"))
        self.assertFalse(interpreter.can_load("json"))
        content2 = interpreter.load(os.path.join(self.folder, "example.txt"))
        self.assertEqual(content, content2)

    def test_interpreters_inference(self):
        interpreters = Interpreters()
        interpreters.register(TextInterpreter())
        interpreters.register(JSONInterpreter())
        interpreters.register(BinaryInterpreter())

        with open(os.path.join(self.folder, "example"), "wb") as f:
            f.write(b"content!")

        with open(os.path.join(self.folder, "example.txt"), "w") as f:
            f.write("content!")

        with open(os.path.join(self.folder, "example.json"), "w") as f:
            json.dump({"content": "content!"}, f)

        self.assertEqual(interpreters.load(os.path.join(self.folder, "example")), b"content!")
        self.assertEqual(interpreters.load(os.path.join(self.folder, "example.txt")), "content!")
        self.assertEqual(interpreters.load(os.path.join(self.folder, "example.json")), {"content": "content!"})

        # Same with save
        interpreters.save(os.path.join(self.folder, "example2"), b"content!")
        with open(os.path.join(self.folder, "example2"), "rb") as f:
            content = f.read()
        self.assertEqual(content, b"content!")

        interpreters.save(os.path.join(self.folder, "example2.txt"), "content!")
        with open(os.path.join(self.folder, "example2.txt"), "r") as f:
            content = f.read()
        self.assertEqual(content, "content!")

        interpreters.save(os.path.join(self.folder, "example2.json"), {"content": "content!"})
        with open(os.path.join(self.folder, "example2.json"), "r") as f:
            content = json.load(f)
        self.assertEqual(content, {"content": "content!"})

        # An invalid object can't be saved
        with self.assertRaises(Exception):
            interpreters.save(os.path.join(self.folder, "example2.txt"), 55)

        # If a file does not exist, error raised
        with self.assertRaises(Exception):
            interpreters.load("unknown")

if __name__ == '__main__':
    unittest.main()