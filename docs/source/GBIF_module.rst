GBIF Module
===========

.. _GBIF_module:

.. _GBIF: https://www.gbif.org/
.. _species/search: https://techdocs.gbif.org/en/openapi/v1/species#/
.. _Anax imperator Leach, 1815: https://api.gbif.org/v1/species/search?datasetKey=d7dddbf4-2cf0-4f39-9b2a-bb099caae36c&q=Anax%20imperator%20Leach,%201815&limit=20


Overview
^^^^^^^^

The **GBIF module** allows users to easily retrieve occurrence information about taxa from the Global Biodiversity
Information Facility `GBIF`_ database. The information is downloaded in JSON format.


Key Features
^^^^^^^^^^^^

- *Retrieve GBIF scientific nomenclature.* Users can obtain the scientific nomenclature of a taxon by accessing the GBIF
  Backbone Taxonomy and retrieving its taxonomic classification.
- *Retrieve occurrences.* Users can obtain occurrences of a taxon by accessing GBIF data to gather information on its
  geographic distribution and associated metadata.

Retrieve nomenclature information and associated metadata about a taxon from the GBIF
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this example, we set the `dataset_key` to correspond with the GBIF Backbone Taxonomy and specify a `limit` of 20
results per page. Moreover, we extract only the accepted name using the parameter `accepted_only` as *True*.
This function utilizes the GBIF API's endpoint `species/search`_.


.. warning::
If the parameter accepted_only is set to False, the search results may include taxa that do not match the intended search.
For example, when searching for `Anax imperator Leach, 1815`_ with this parameter set to False, the results may include
unrelated taxa, such as the second record in the example, which is an Ephemeroptera rather than an Odonate.
Please review the results carefully.


.. code-block:: python
    from biodumpy import Biodumpy
    from biodumpy.inputs import GBIF

    # GBIF dataset key
    gbif_backbone = 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c'

    # Taxa list
    taxa = ['Alytes muletensis (Sanchíz & Adrover, 1979)', 'Bufotes viridis (Laurenti, 1768)',
            'Hyla meridionalis Boettger, 1874', 'Anax imperator Leach, 1815']

    bdp = Biodumpy([GBIF(dataset_key=gbif_backbone, limit=20, bulk=False, accepted_only=True, occ=False)])
    bdp.start(taxa, output_path='YOUR_OUTPUT_PATH/downloads/{date}/{module}/{name}')


Extract main information from a JSON downloaded file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users can easily filter the data by loading the JSON file and selecting the required fields.
In this example, we retrieve the taxon's taxonomy, GBIF taxon key, taxonomic status, and taxonomic rank.

.. code-block:: python
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


Retrieve occurrences and associated metadata about a taxon from the GBIF
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This function provides also the ability to download occurrences for a specific taxon. By setting the parameter **occ**
to True, users can enable the download of these occurrences. Additionally, the function supports filtering occurrences
based on a specified geographic region using the `geometry` parameter.
When `geometry` is provided, only occurrences that fall within the defined polygon are included in the result.
Here we provide an example to extract the main information from downloaded data.

.. code-block:: python
    from biodumpy import Biodumpy
    from biodumpy.inputs import GBIF
    import json

    # Download data
    gbif_backbone = 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c'
    poly = 'POLYGON((0.248 37.604, 6.300 37.604, 6.300 41.472, 0.248 41.472, 0.248 37.604))'

    taxa = ['Alytes muletensis (Sanchíz & Adrover, 1979)', 'Bufotes viridis (Laurenti, 1768)',
            'Hyla meridionalis Boettger, 1874', 'Anax imperator Leach, 1815']

    bdp = Biodumpy([GBIF(dataset_key=gbif_backbone, limit=20, bulk=False, accepted_only=True, occ=True, geometry=poly)])
    bdp.start(taxa, output_path='YOUR_OUTPUT_PATH/downloads/{date}/{module}/{name}')

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
