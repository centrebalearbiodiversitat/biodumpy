GBIF Module
===========

.. _GBIF:


Overview
--------

The ``GBIF`` module allows users to easily retrieve data information from the Global Biodiversity Information Facility
(`GBIF`_) database. The information is downloaded in JSON format.

.. _GBIF: https://www.gbif.org/

Key Features
------------

- **Retrieve GBIF scientific nomenclature.** Users can obtain the scientific nomenclature of a taxon by accessing the GBIF
  Backbone Taxonomy and retrieving its taxonomic classification.
- **Retrieve occurrences.** Users can obtain occurrences of a taxon by accessing GBIF data to gather information on its
  geographic distribution and associated metadata.


Retrieve nomenclature information and associated metadata from GBIF
-------------------------------------------------------------------

In this example we demonstrated how download taxonomic nomenclature for a list of taxa from GBIF.
We set the ``dataset_key`` to correspond with the GBIF Backbone Taxonomy and specify a ``limit`` of 20 results per page.
Moreover, we extract only the accepted name using the parameter ``accepted_only`` to *True*.
This function utilizes the GBIF API's endpoint `species/search`_.

.. _species/search: https://techdocs.gbif.org/en/openapi/v1/species#/

.. note::

    The taxonomy list should be compiled using the taxon names with the authorship information to avoid nomenclature issues.

.. warning::

    If the parameter ``accepted_only`` is set to *False*, the search results may include taxa that do not match the intended search.
    For example, when searching for `Anax imperator Leach, 1815`_ with this parameter set to *False*, the results may include
    unrelated taxa, such as the second record in the example, which is an Ephemeroptera rather than an Odonate.
    **Please review the results carefully.**

.. _Anax imperator Leach, 1815: https://api.gbif.org/v1/species/search?datasetKey=d7dddbf4-2cf0-4f39-9b2a-bb099caae36c&q=Anax%20imperator%20Leach,%201815&limit=20


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import GBIF

    # GBIF dataset key
    gbif_backbone = 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c'

    # Taxa list
    taxa = ['Alytes muletensis (Sanchíz & Adrover, 1979)', 'Bufotes viridis (Laurenti, 1768)',
            'Hyla meridionalis Boettger, 1874', 'Anax imperator Leach, 1815']

    # Set the module and start the download
    bdp = Biodumpy([GBIF(dataset_key=gbif_backbone, limit=20, bulk=False, accepted_only=True, occ=False)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')


Extract main information from downloaded file
---------------------------------------------

Users can easily filter the data by loading the JSON file downloaded and selecting the required fields.
In this example, we retrieve the taxonomy, GBIF taxon key, taxonomic status, and taxonomic rank of a taxon.

In this case, we retrieve information for a single taxon because we set the ``bulk`` parameter to *False* in the previous
code block. However, the following script is also applicable for processing bulk files. In the latter case, we obtain
an object that contains all the taxa.

.. code-block:: python

    import json

    # Load the downloaded JSON file
    file = 'YOUR_JSON_PATH'
    with open(file, 'r') as f:
        data = json.load(f)

    # The strings in the get function correspond to the key of the JSON.
    filtered_data = []
    for entry in data:
        filtered_data.append({'key': entry.get('key', None),
                              'kingdom': entry.get('kingdom', None),
                              'phylum': entry.get('phylum', None),
                              'class': entry.get('class', None),
                              'order': entry.get('order', None),
                              'family': entry.get('family', None),
                              'genus': entry.get('genus', None),
                              'species': entry.get('species', None),
                              'scientificName': entry.get('scientificName', None),
                              'taxonomicStatus': entry.get('taxonomicStatus', None),
                              'rank': entry.get('rank', None)})


Retrieve occurrences and associated metadata from GBIF
------------------------------------------------------

The ``GBIF`` module provides also the ability to download occurrences for a specific taxon. By setting the parameter
``occ`` to *True*, users can enable the download of these occurrences.
Additionally, the module supports filtering occurrences based on a specified geographic region using the ``geometry``
parameter. When a ``geometry`` is provided, only occurrences that fall within the defined polygon are included in the
result. Here we provide an example to download and extract the main information from downloaded dataset.

.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import GBIF
    import json

    # Download data
    gbif_backbone = 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c'

    # Set the polygon
    poly = 'POLYGON((0.248 37.604, 6.300 37.604, 6.300 41.472, 0.248 41.472, 0.248 37.604))'

    # Taxa list
    taxa = ['Alytes muletensis (Sanchíz & Adrover, 1979)', 'Bufotes viridis (Laurenti, 1768)',
            'Hyla meridionalis Boettger, 1874', 'Anax imperator Leach, 1815']

    # Set the module and start the download
    bdp = Biodumpy([GBIF(dataset_key=gbif_backbone, limit=20, bulk=False, accepted_only=True, occ=True, geometry=poly)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')

    # Retrieve main information
    file = 'YOUR_JSON_PATH'
    with open(file, 'r') as f:
        data = json.load(f)

    filtered_data = []
    for entry in data:
        filtered_data.append({'key': entry.get('key', None),
                              'kingdom': entry.get('kingdom', None),
                              'phylum': entry.get('phylum', None),
                              'class': entry.get('class', None),
                              'order': entry.get('order', None),
                              'family': entry.get('family', None),
                              'genus': entry.get('genus', None),
                              'species': entry.get('species', None),
                              'scientificName': entry.get('scientificName', None),
                              'taxonomicStatus': entry.get('taxonomicStatus', None),
                              'rank': entry.get('rank', None),
                              'basisOfRecord': entry.get('basisOfRecord', None),
                              'lifeStage': entry.get('lifeStage', None),
                              'decimalLatitude': entry.get('decimalLatitude', None),
                              'decimalLongitude': entry.get('decimalLongitude', None),
                              'coordinateUncertaintyInMeters': entry.get('coordinateUncertaintyInMeters', None),
                              'continent': entry.get('continent', None),
                              'stateProvince': entry.get('stateProvince', None),
                              'locality': entry.get('locality', None),
                              'year': entry.get('year', None)
                              })


Reference link/s
----------------

`Global Biodiversity Information Facility`_

.. _Global Biodiversity Information Facility: https://www.gbif.org/