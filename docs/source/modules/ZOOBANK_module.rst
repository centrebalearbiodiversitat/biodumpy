ZOOBANK Module
==============

.. _ZOOBANK_module:


Overview
--------

The ``ZOOBANK`` module allows users to easily retrieve scientific bibliographic information about taxa from the Official
Registry of Zoological Nomenclature (ZooBank) database. By providing a taxa name, users can access bibliographic data.
The information is downloaded in JSON format.

Key Features
------------

- **Retrieve scientific bibliographic information**. Access to bibliography stored in ZooBank of specific taxa.


Retrieve comprehensive metadata from BOLD
-----------------------------------------

This example demonstrates how users can download bibliographic information from ZooBank for a list of taxa.
When the ``dataset_size`` parameter is set to *small*, the function relies on the ZooBank API's `References`_ endpoint.
However, if ``dataset_size`` is set to *large*, the function connects to the ZooBank website and retrieves the information
through a web scraping process. As a result, the output file may vary slightly depending on whether a *small* or *large*
dataset size is selected.

.. _References: http://zoobank.org/References.json?term=pyle

.. note::

    The taxonomy list should be compiled using only the taxon names, excluding any authorship information.


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import ZOOBANK

    # Taxa list
    taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis', 'Anax imperator']

    # Set the module and start the download
    # Start the download
    bdp = Biodumpy([ZOOBANK(bulk=False, dataset_size='small', info=False)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')


Reference link/s
----------------

`Official Registry of Zoological Nomenclature`_

.. _Official Registry of Zoological Nomenclature: https://zoobank.org/