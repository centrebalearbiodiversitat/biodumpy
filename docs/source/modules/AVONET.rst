AVONET Module
===========

.. _AVONET_module:


Overview
--------

The ``AVONET`` module allows users to easily retrieve data information from the AVONET (`AVONET`_) dataset :cite:`tobias2022avonet`.

This module uses a plug-in file containing information from the AVONET dataset. The file will be downloaded the first time the module is used and whenever the package is updated or modified.
Specifically, the data are retrieved from the file AVONET1_BirdLife, available at https://figshare.com/s/b990722d72a26b5bfead.

.. _AVONET: https://doi.org/10.1111/ele.13898

.. toggle:: Click to expand

    JSON


Key Features
------------

- **Retrieve information from AVONET.** Users can retrieve the information from AVONET dataset.

Retrieve metadata from AVONET
-----------------------------

In this example, we obtain the information from AVONET setting the parameter ``bulk`` to *True*. 

.. note::

    The taxonomy list should be compiled using only taxon names, excluding any authorship information. Species names must match those present in the AVONET dataset.


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import AVONET

    # Taxa list
    taxa = ['Accipiter albogularis', 'Accipiter fasciatus', 'Accipiter tachiro']

    # Set the module and start the download
    bdp = Biodumpy([AVONET(bulk=True, output_format="json")])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')


Reference link/s
----------------

`AVONET`_

.. _AVONET: https://doi.org/10.1111/ele.13898
