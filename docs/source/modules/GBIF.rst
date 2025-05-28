GBIF Module
===========

.. _GBIF_module:


Overview
--------

The ``GBIF`` module allows users to easily retrieve data information from the Global Biodiversity Information Facility (`GBIF`_) database :cite:`gbif2024`.

.. _GBIF: https://www.gbif.org/

.. toggle:: Click to expand

    JSON


Key Features
------------

- **Retrieve GBIF scientific nomenclature.** Users can obtain the scientific nomenclature of a taxon by accessing the GBIF Backbone Taxonomy and retrieving its taxonomic classification.
- **Retrieve occurrences.** Users can obtain occurrences of a taxon by accessing GBIF data to gather information on its geographic distribution and associated metadata.


Retrieve nomenclature information and associated metadata from GBIF
-------------------------------------------------------------------

In this example we demonstrated how download taxon nomenclature for a list of taxa from GBIF. We set the ``dataset_key`` to correspond with the GBIF Backbone Taxonomy and specify a ``limit`` of 20 results per page. Moreover, we extract only the accepted name using the parameter ``accepted_only`` to *True*. This function utilizes the GBIF API's endpoint `/species`_.

.. _/species: https://api.gbif.org/v1/species?

.. note::

     The taxonomy list should be compiled using only the taxon names, excluding any authorship information.


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import GBIF

    # GBIF dataset key
    gbif_backbone = 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c'

    # Taxa list
    taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis', 'Anax imperator']

    # Set the module and start the download
    bdp = Biodumpy([GBIF(dataset_key=gbif_backbone, limit=20, bulk=False, accepted_only=True, occ=False)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')


Retrieve occurrences and associated metadata from GBIF
------------------------------------------------------

The ``GBIF`` module provides also the ability to download occurrences for a specific taxon. By setting the parameter ``occ`` to *True*, users can enable the download of these occurrences. Additionally, the module supports filtering occurrences based on a specified geographic region using the ``geometry`` parameter. When a ``geometry`` is provided, only occurrences that fall within the defined polygon are included in the result. Here we provide an example to download and extract the main information from downloaded dataset.

.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import GBIF
    import json

    # Download data
    gbif_backbone = 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c'

    # Set the polygon
    poly = 'POLYGON((0.248 37.604, 6.300 37.604, 6.300 41.472, 0.248 41.472, 0.248 37.604))'

    # Taxa list
    taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis', 'Anax imperator']

    # Set the module and start the download
    bdp = Biodumpy([GBIF(dataset_key=gbif_backbone, limit=20, bulk=False, accepted_only=True, occ=True, geometry=poly)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')

Reference link/s
----------------

`Global Biodiversity Information Facility`_

.. _Global Biodiversity Information Facility: https://www.gbif.org/