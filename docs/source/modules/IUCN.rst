IUCN Module
===========

.. _IUCN_module:


Overview
--------

The ``IUCN`` module allows users to easily retrieve information about species assessments, habitats, and threats from the IUCN :cite:`iucn2024`. By providing the taxon name and an API key, users can access the desired data. For more details on obtaining API keys and accessing the documentation, please visit the IUCN Red List API v4 (`IUCN_API`_).

.. _IUCN_API: https://api.iucnredlist.org/

.. toggle:: Click to expand

    JSON


Key Features
------------

- **Retrieve general IUCN information**: Access general data about a taxon, including its conservation status, habitats, and threats.


Retrieve IUCN information
-------------------------

Users can download IUCN information for a specific taxon and select one or more IUCN regions to filter the data based on specific geographic delimitations within the IUCN.

.. note::

    The taxonomy list should include only the taxon names, excluding any authorship information. If the taxon is a subspecies or subpopulation, you must explicitly specify whether it is a subspecies. A message will be displayed in the terminal during the download.


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import IUCN

    # Insert your api_key
    api_key = 'YOUR_API_KEY'

    # Taxa list
    taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis', 'Anax imperator', 'Equus ferus przewalskii']

    # Create a list containing the IUCN regions
    regions = ['Global', 'Europe']

    # Set the module and start the download
    bdp = Biodumpy([IUCN(authorization=api_key, bulk=True, scope=regions)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')


Reference link/s
----------------

`IUCN Red List of Threatened Species`_

.. _IUCN Red List of Threatened Species: https://www.iucnredlist.org/
