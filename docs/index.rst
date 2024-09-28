.. pybmd documentation master file, created by
   sphinx-quickstart on Mon Aug  1 13:09:36 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root ``toctree`` directive.

PyBMD
=================================
Python wrapper library for DaVinci Resolve API

How To Install
--------------------
.. code-block:: python

   pip install pybmd

How To Use
-------------
**Run Davinci Resolve before you run script**

.. code-block:: python

   from pybmd import Resolve
   LOCAL_RESOLVE = Resolve()

``Resolve()`` has an option arg named ``resolve_ip`` , default value is ``127.0.0.1`` stands for local davinci, if you want to use remote DaVinci Resolve object, change arg to remote ip.

API Reference
----------------

.. toctree::
   :maxdepth: 2

   reference

Samples
-----------

.. toctree:: 

   samples




