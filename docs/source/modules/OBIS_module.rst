GBIF Module
===========

.. _OBIS_module:


Overview
--------

The ``OBIS`` module allows users to easily retrieve data information from the Ocean Biodiversity Information System
(`OBIS`_) database. The information is downloaded in JSON format.

.. _OBIS: https://obis.org/

Key Features
------------

- **Retrieve OBIS scientific nomenclature.** Users can obtain the scientific nomenclature of a taxon by accessing the OBIS
  taxonomy and retrieving its taxonomic classification.
- **Retrieve occurrences.** Users can obtain occurrences of a taxon by accessing OBIS data to gather information on its
  geographic distribution and associated metadata.


Retrieve nomenclature information and associated metadata from OBIS
-------------------------------------------------------------------

In this example we demonstrated how download taxonomic nomenclature for a list of taxa from OBIS. This database
contains only **marine** species. Thus we use as reference list three taxa belonging the classes Bivalvia, Mammalia, and
Anthozoa. This function utilizes the OBIS API's endpoint `/taxon/`_.

.. _/taxon/: https://api.obis.org/v3/taxon/

.. note::

    The taxonomy list should be compiled using only the taxon names, excluding any authorship information.


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import OBIS

    # Taxa list
    taxa = ['Delphinus delphis', 'Pinna nobilis', 'Plerogyra sinuosa']

    # Set the module and start the download
    bdp = Biodumpy([OBIS(bulk=False, occ=False)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')


Extract main information from downloaded file
---------------------------------------------

Users can easily filter the data by loading the JSON file downloaded and selecting the required fields.
In this example, we retrieve the taxonomy, OBIS taxonID, taxonomic status, and taxonomic rank of a taxon.

In this example, we retrieve information for a single taxon because we set the ``bulk`` parameter to *False* previously
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
        filtered_data.append({'taxonID': entry.get('taxonID', None),
                              'kingdom': entry.get('kingdom', None),
                              'phylum': entry.get('phylum', None),
                              'class': entry.get('class', None),
                              'order': entry.get('order', None),
                              'family': entry.get('family', None),
                              'genus': entry.get('genus', None),
                              'species': entry.get('species', None),
                              'scientificName': entry.get('scientificName', None),
                              'taxonomicStatus': entry.get('taxonomicStatus', None),
                              'taxonRank': entry.get('taxonRank', None)})


Retrieve occurrences and associated metadata from OBIS
------------------------------------------------------

The ``OBIS`` module provides also the ability to download occurrences for a specific taxon. By setting the parameter
``occ`` to *True*, users can enable the download of these occurrences.
Additionally, the module supports filtering occurrences based on a specified geographic region using either the
``geometry`` or ``areaid`` parameters. These parameters can be used separately or together.
When a ``geometry`` or ``areaid`` are provided, only occurrences that fall within the defined polygons are included in the
result. Here we provide an example to download and extract the main information from downloaded dataset.

.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import OBIS
    import json

    # Set the polygon
    poly = 'POLYGON((0.248 37.604, 6.300 37.604, 6.300 41.472, 0.248 41.472, 0.248 37.604))'
    areaid = 33322 # This is the Balearic sea

    # Taxa list
    taxa = ['Delphinus delphis', 'Pinna nobilis', 'Plerogyra sinuosa']

    # Set the module and start the download occurrences
    bdp = Biodumpy([OBIS(bulk=False, occ=True)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}_occ/{name}')

    # Set the module and start the download occurrences within a polygon
    bdp = Biodumpy([OBIS(bulk=False, occ=True, geometry=poly)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}_poly/{name}')

    # Set the module and start the download occurrences within an area
    bdp = Biodumpy([OBIS(bulk=False, occ=True, geometry=None, areaid=areaid)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}_area/{name}')

    # Set the module and start the download occurrences within a polygon inside an area
    bdp = Biodumpy([OBIS(bulk=False, occ=True, geometry=poly, areaid=areaid)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}_area_poly/{name}')


Reference link/s
----------------

`Ocean Biodiversity Information System`_

.. _Ocean Biodiversity Information System: https://obis.org/