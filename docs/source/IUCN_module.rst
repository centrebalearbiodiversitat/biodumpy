IUCN Module
===========

.. _IUCN_module:

.. _IUCN_API: https://apiv3.iucnredlist.org/api/v3/docs#regions

Overview
--------

The **IUCN module** allows users to easily retrieve information about species assessments, habitats, and threats from the IUCN.
By providing the species name and API keys, users can access comprehensive data. The information is downloaded in JSON format.
For more details on obtaining API keys and accessing the documentation, please visit the IUCN Red List API v3 (`IUCN_API`_).


Key Features
^^^^^^^^^^^^

- **Retrieve IUCN information about a species.** Access general data about the species, including its conservation status.
- **Retrieve IUCN habitat information about a species.** Get detailed information about the natural habitats of the species.
- **Retrieve IUCN historical assessments about a species.** Obtain historical data on the species' conservation status over time.
- **Retrieve IUCN threat information about a species.** Identify threats impacting the species and their severity.

Retrieve IUCN information about a species
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users can download IUCN information for a specific species and select one or more IUCN regions to filter the data based
on specific geographic delimitations within the IUCN. Regions should be provided as a list in the region parameter.
For more details on the IUCN regions list, visit the endpoint */api/v3/region/list?token='YOUR TOKEN'* in the
IUCN Red List API v3 (`IUCN_API`_).


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import IUCN

    # Insert your api_key
    api_key = 'YOUR_API_KEY'

    # Taxa list
    taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis']

    # Select your output path
    output_path = 'YOUR_OUTPUT_PATH'

    # Select the regions
    regions = ['global', 'europe']

    bdp = Biodumpy([IUCN(api_key=api_key, bulk=True, region=regions)])
    bdp.start(taxa, output_path=output_path)


Retrieve habitat information about a species
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users can retrieve information about IUCN species habitat setting the parameter ``habitat`` as *True*.

.. code-block:: python

    bdp = Biodumpy([IUCN(api_key=api_key, bulk=True, region=regions, habitat=True)])
    bdp.start(taxa, output_path=output_path)


Retrieve historical assessments about a species
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To obtain the historical assessments of the species, users can set the parameter ``historical`` as *True*.

.. code-block:: python

    bdp = Biodumpy([IUCN(api_key=api_key, bulk=True, region=regions, historical=True)])
    bdp.start(taxa, output_path=output_path)


Retrieve threat information about a species
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Threaths information about a species is downloadable setting the parameter ``threats`` as *True*.

.. code-block:: python

    bdp = Biodumpy([IUCN(api_key=api_key, bulk=True, region=regions, threats=True)])
    bdp.start(taxa, output_path=output_path)


<hr>
<div style="display: flex; justify-content: center">
<img src='/www/logo_cbb.png' alt='logo_cbb' width='200'>
</div>



