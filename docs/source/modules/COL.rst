COL Module
==========

.. _COL:


Overview
--------

The ``COL`` module enables users to easily retrieve nomenclature information from the Catalogue of Life (`COL`_)
database. The information will be downloaded in JSON format.

.. _COL: https://www.catalogueoflife.org/

Key Features
------------

- **Retrieve nomenclature information from COL database.** Users can access the nomenclature details of a given taxon stored in the COL database.
- **Check for synonym.** Users can obtain the accepted nomenclature of a given taxon if it is listed as a synonym in the COL database.


Retrieve nomenclature from COL - Only accepted names
----------------------------------------------------

In this first example, we download the nomenclature from COL for a list of taxa by setting the ``bulk`` parameter to *True*.
In this case, the list of taxa consists only of accepted names. This function utilizes the COL ChecklistBankAPI
endpoint `nameusage/search?`_.

.. _nameusage/search?: https://api.checklistbank.org/dataset/9923/nameusage/search?


.. note::

    The taxonomy list should be compiled using only the taxon names, excluding any authorship information.


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import COL

    # List od taxa
    taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis', 'Anax imperator']

    # Start the download
    bdp = Biodumpy([COL(bulk=True, check_syn=False)])
    bdp.start(taxa, output_path='/Users/tcanc/PycharmProjects/biodumpy/downloads/{date}/{module}/{name}')


Retrieve nomenclature from COL - With synonym names
---------------------------------------------------

In the following example, the species *Bufo roseus* is a synonym of *Bufotes viridis*.
Here, we test the difference in the results by setting the parameter ``check_syn`` to *False* or *True*.

.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import COL

    # List od taxa
    taxa = ['Bufo roseus']

    # Start the download check_syn = False
    bdp = Biodumpy([COL(bulk=False, check_syn=False)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}_false')

    # Start the download check_syn = True
    bdp = Biodumpy([COL(bulk=False, check_syn=True)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}_true')


When the parameter ``check_syn`` is set to *False*, the ``COL`` module provides both the accepted name and the synonym at the
species level. However, when ``check_syn`` is set to *True*, the results include only the accepted name.

``check_syn = False``

.. code-block:: json

    {
        "id": "NPMS",
        "name": "Bufotes viridis",
        "rank": "species",
        "label": "Bufotes viridis",
        "labelHtml": "<i>Bufotes viridis</i>"
    },
    {
        "id": "NPDX",
        "name": "Bufo roseus",
        "rank": "species",
        "label": "Bufo roseus",
        "labelHtml": "<i>Bufo roseus</i>"
    }


``check_syn = True``

.. code-block:: json

    {
        "id": "NPMS",
        "name": "Bufotes viridis",
        "rank": "species",
        "label": "Bufotes viridis",
        "labelHtml": "<i>Bufotes viridis</i>"
    }


Retrieve nomenclature from COL - Taxon with multiple IDs
--------------------------------------------------------

Sometimes, in the COL database, the same taxon can have multiple IDs. In such cases, the ``COL`` module allows users
to select a specific ID. We recommend choosing the ID after verifying it on the COL website. We can try this option with
the species *Stollia betae*.

.. warning::

    Occasionally, the IDs proposed by the ``COL`` module may differ from those provided by COL after a search.
    If this occurs, or if users encounter difficulties to find the correct ID, select the option *Skip*.


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import COL

    # List od taxa
    taxa = ['Stollia betae']

    # Start the download
    bdp = Biodumpy([COL(bulk=False, check_syn=True)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')



Reference link/s
----------------

`Catalogue of Life`_

.. _Catalogue of Life: https://www.catalogueoflife.org/

