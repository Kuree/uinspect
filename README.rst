uinspect
========

This is a small Python package that offers :sub:`fast` runtime inspection similar to that of ``inspect`` module in Python. To install, simply do

::

   pip install uinspect

benchmark
=========

The following benchmark is generated from running the scripts in ``benchmark/``.

+-----------------+----------------------------------------------+------------------------------+---------+---------+--------------+
| Task name       | uinspect method1                             | uinspect method2             | inspect | speedup | Cost (us/op) |
+=================+==============================================+==============================+=========+=========+==============+
| Source location | ``uinspect.get_location()`` - 0.21s          | ``uinspect.Frame()`` - 0.48s | 16.43s  | 79.7x   | 0.21 us/op   |
+-----------------+----------------------------------------------+------------------------------+---------+---------+--------------+
| Locals          | ``uinspect.Frame().locals`` - 0.99s          | N/A                          | 0.82s   | 0.82x   | 0.99 us/op   |
+-----------------+----------------------------------------------+------------------------------+---------+---------+--------------+
| Locals diff     | ``uinspect.Frame(2).collect_vars()`` - 2.94s | N/A                          | 1.20s   | 0.41x   | 2.94 us/op   |
+-----------------+----------------------------------------------+------------------------------+---------+---------+--------------+

It turns out that the ``uinspect`` does not speed up the local variable calculation. This is because we have to run an expensive Python C API call regardless of whether it’s ``uinspect`` or ``inspect``. As a result, the overhead is caused by the fact that ``uinspect`` needs to convert Python object to C++ object.

The lesson is to use ``inspect`` module for any local variables related manipulation since it’s faster, but use ``uinspect`` to obtain source location.