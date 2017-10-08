#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyfolder import PyFolder

__author__ = "Iván de Paz Centeno"

pyfolder = PyFolder("/home/ivan/examplesss", allow_override=True, allow_remove_folders_with_content=True)

pyfolder['example/example/pepe.txt'] = "222"

"""print(pyfolder['example']['example']['pepe.txt'])
print(pyfolder['example/example/pepe.txt'])
print(pyfolder['yo.txt'])
print(pyfolder['jeje.json'])

del pyfolder['example/example/pepe.txt']
del pyfolder['example']['example']['pepe.txt']
del pyfolder['example']['example']
del pyfolder['.']
"""