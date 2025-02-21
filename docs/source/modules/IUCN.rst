IUCN Module
===========

.. _IUCN_module:


Overview
--------

The ``IUCN`` module allows users to easily retrieve information about species assessments, habitats, and threats from the IUCN :cite:`iucn2024`. By providing the taxon name and an API key, users can access the desired data. For more details on obtaining API keys and accessing the documentation, please visit the IUCN Red List API v3 (`IUCN_API`_).

.. _IUCN_API: https://apiv3.iucnredlist.org/api/v3/docs#regions

.. toggle:: Click to expand

    JSON


Key Features
------------

- **Retrieve general IUCN information.** Access general data about a taxon, including its conservation status.
- **Retrieve IUCN habitat information.** Get detailed information about the natural habitats of a taxon.
- **Retrieve IUCN historical assessments.** Obtain historical data on the taxon's conservation status over time.
- **Retrieve IUCN threat information.** Identify threats impacting the taxon and their severity.


Retrieve general IUCN information
---------------------------------

Users can download IUCN information for a specific species and select one or more IUCN regions to filter the data based on specific geographic delimitations within the IUCN. Regions should be provided as a list in the region parameter. For more details on the IUCN regions list, visit the endpoint **/api/v3/region/list?token='YOUR TOKEN'** in the IUCN Red List API v3 (`IUCN_API`_).

.. note::

    The taxonomy list should be compiled using only the taxon names, excluding any authorship information.


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import IUCN

    # Insert your api_key
    api_key = 'YOUR_API_KEY'

    # Taxa list
    taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis', 'Anax imperator']

    # Create a list containing the IUCN regions
    regions = ['global', 'europe']

    # Set the module and start the download
    bdp = Biodumpy([IUCN(api_key=api_key, bulk=True, region=regions)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')


Retrieve IUCN habitat information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Users can retrieve information about IUCN species habitat setting the parameter ``habitat`` to *True*.

.. code-block:: python

    bdp = Biodumpy([IUCN(api_key=api_key, bulk=True, region=regions, habitat=True)])
    bdp.start(taxa, output_path=output_path)


Retrieve IUCN historical assessments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To obtain the historical assessments of the species, users can set the parameter ``historical`` to *True*.

.. code-block:: python

    bdp = Biodumpy([IUCN(api_key=api_key, bulk=True, region=regions, historical=True)])
    bdp.start(taxa, output_path=output_path)


Retrieve IUCN threat information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Threats information about a species is downloadable setting the parameter ``threats`` to *True*.

.. code-block:: python

    bdp = Biodumpy([IUCN(api_key=api_key, bulk=True, region=regions, threats=True)])
    bdp.start(taxa, output_path=output_path)


Retrieve IUCN citation and weblink
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The citation for a given species assessment and the redirection link are downloadable by setting the parameters ``citation`` and ``weblink`` to *True*.

.. code-block:: python

    bdp = Biodumpy([IUCN(api_key=api_key, bulk=True, region=regions, weblink=True, citation=True)])
    bdp.start(taxa, output_path=output_path)


Reference link/s
----------------

`IUCN Red List of Threatened Species`_

.. _IUCN Red List of Threatened Species: https://www.iucnredlist.org/
