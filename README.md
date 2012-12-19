About
=====

A simple pure Python wrapper around Thread()s.

Installation
============

taskqueue is available from PyPI

    easy_install taskqueue

Basic Usage
===========

For a simple example look in the examples folder.

Documentation
=============

These are the parts you need to know about.
Everything else can be looked up in the code.



Queue
-----
This is the task and worker manager.
It is in itself a python Thread and manages the incoming Tasks,
runs them, and makes them available when they're finished.



**add(target, *args)**

You use this to add new Tasks to the queue.

Pass a function/method pointer as the target parameter and
provide the necessary arguments in *args.

*It does not currently accept keyword args.*



**finished**

This provides an iterator that yields the Tasks in the Queue
as they finish.

No need to wait for the tasks to finish before accessing them.
Just call this and they will be delivered as they are done.



Task
----
This is the task representation and is also a python Thread.

**result**

This is the only thing you need from a task.
It holds the return result of the task.



LICENSE
=======

taskqueue is released under the [MIT License](http://www.opensource.org/licenses/mit-license.php).
