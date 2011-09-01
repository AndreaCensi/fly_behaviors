.. raw:: html
   :file: fork.html

.. include:: definitions.txt

.. py:currentmodule:: fly_behaviors

FlyBehaviors
=============

|FlyBehaviors| is a Python package for simulating vision-based insect behaviors.



Simple usage example: ::
  
      $ fly_behaviors_corridor
      $ pg -m procgraph_vehicles veh_yaml2movie file=last.yaml output=last.avi
      
**Support**: use the GitHub issue tracker_.

**Documentation index**

- :ref:`installation` 
- :ref:`api` 
- :ref:`api_reference`
- :ref:`credits`


.. _tracker: http://github.com/AndreaCensi/fly_behaviors/issues

.. _me: http://www.cds.caltech.edu/


.. _installation:

Installation
------------

Install |FlyBehaviors| using: ::

    $ pip install FlyBehaviors
    
.. raw:: html
   :file: download.html

TYou can download this project in either zip_ or tar_ formats, or 
download using git: ::

    $ git clone git://github.com:AndreaCensi/fly_behaviors.git

Install using: ::

    $ python setup.py develop
    $ nosetests -w src         # run the extensive test suite


.. _tar:: http://github.com/AndreaCensi/fly_behaviors/tarball/master
.. _zip:: http://github.com/AndreaCensi/fly_behaviors/zipball/master


.. include:: api.rst.inc


 

