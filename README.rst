==============
pyfolder 0.0.1
==============

`PyFolder` is a package for managing a filesystem folders as a dictionary.

.. image:: https://badge.fury.io/py/pyfolder.svg
    :target: https://badge.fury.io/py/pyfolder

.. image:: https://travis-ci.org/ipazc/pyfolder.svg?branch=master
    :target: https://travis-ci.org/ipazc/pyfolder

.. image:: https://coveralls.io/repos/github/ipazc/pyfolder/badge.svg?branch=master
    :target: https://coveralls.io/github/ipazc/pyfolder?branch=master

.. image:: https://landscape.io/github/ipazc/pyfolder/master/landscape.svg?style=flat
   :target: https://landscape.io/github/ipazc/pyfolder/master
   :alt: Code Health


Installation
============
Currently it is only supported **Python 3.4.1** onwards:

.. code:: bash

    sudo pip3 install pyfolder


Example
=======
.. code:: python

    >>> from pyfolder import PyFolder
    >>> 
    >>> pyfolder = PyFolder("/path/to/folder")
    >>> pyfolder["file.txt"] = "hello, this is going to be instantly the content of this file."

Basic Usage
===========
`PyFolder` can easily store or read content from the filesystem. The usage is the same as a normal dictionary:

* Create a file with specific binary content:

.. code:: python

    >>> from pyfolder import PyFolder
    >>> 
    >>> pyfolder = PyFolder("/path/to/folder")
    >>> pyfolder['file.bin'] = b"Content as bytes"
    >>> pyfolder['file.txt'] = "Content as text"
    >>> pyfolder['file.json'] = {"content": "Content as JSON"}
    >>> pyfolder['file.jpg'] = PILImage


`PyFolder` automatically detects the kind of content to store.

It is also possible to reference the creation of a file in relative file URI notation:

.. code:: python

    >>> pyfolder["folder1/folder2/file.txt"]

If folder specified doesn't exist, by default it will create it automatically unless the flag `auto_create_folder` is set to `False` during instantiation:

.. code:: python

    >>> pyfolder = PyFolder("/path/to/folder", auto_create_folder=False)

Note that "." or ".." chars are not allowed in URI notation, it must be relative URIs to the root.


* Get specific content:

.. code:: python

    >>> pyfolder = PyFolder("/path/to/folder")
    >>> pyfolder['file.bin']
    b"Content as bytes"
    >>> pyfolder['file.txt']
    "Content as text"
    >>> pyfolder['file.json']
    {"content": "Content as JSON"}
    >>> pyfolder['folder1/folder2/file.bin']
    b"Other content"

By default `PyFolder` will attempt to load the content with the best interpreter it has, based on the file extension. If no interpreter is found for
a content, it will return the content in bytes format. This behaviour can be disabled with the flag `interpret=False` during instantiation:

.. code:: python

    >>> pyfolder = PyFolder("/path/to/folder", interpret=False)


* Edit content:

`PyFolder` won't allow modification or removal of elements unless the flag `allow_override` is specified during instantiation:

.. code:: python

    >>> pyfolder = PyFolder("/path/to/folder", allow_override=True)
    >>> pyfolder['file.bin'] = b"replaced_content_bytes"


* Remove content:

.. code:: python

    >>> del pyfolder['file.bin']


Note that a folder can also be removed:

.. code:: python

    >>> del pyfolder['folder1']
    >>> del pyfolder['.']  # deletes PyFolder root folder


By default PyFolder won't remove a folder unless its content is empty. In order to be able to remove folders without restriction, enable the flag `allow_remove_folders_with_content`

.. code:: python

    >>> pyfolder = PyFolder("/path/to/folder", allow_remove_folders_with_content=True)


* Iterate over folders:

.. code:: python

    >>> for folder_name in pyfolder.folders():
    ...


it is also possible to iterate over the folder name and its content at the same time:


.. code:: python

    >>> for folder_name, folder_content in pyfolder.folders_items():
    ...


In `PyFolder`, each folder is a `PyFolder` object. It is perfectly possible to nest folders as follows:

.. code:: python

    >>> pyfolder["folder1"]["folder2"]
    >>> pyfolder["folder1/folder2"]  # Equivalent in relative URI notation


* Iterate over files:

By default `PyFolder` allows iteration over files, including the folders:

.. code:: python

    >>> for file_name in pyfolder:
    >>>    print(file_name)

If it is wanted to access also the content, it can be done with the `items()` method:

.. code:: python

    >>> for file_name, content in pyfolder.items():
    >>>    print(file_name, content)

If only files are wanted, the `files()` method exists to serve the purpose:

.. code:: python

    >>> for file_name in pyfolder.files()
    ...
    >>> for file_name, content in pyfolder.files_items()


* Search for files:

`PyFolder` eases the search of a file/folder by matching a name. It will return the list of relative URIs of the file-names found:

.. code:: python

    >>> pyfolder.index("name.bin")
    >>> ['path/to/name.bin', 'path2/to/name.bin']


LICENSE
=======

It is released under the MIT license.