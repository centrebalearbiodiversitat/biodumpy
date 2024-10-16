WORMS Module
==========

.. _WORMS_module:


Overview
--------

The ``WORMS`` module enables users to easily retrieve nomenclature information from the World Register of Marine Species (`WoRMS`_) database :cite:`worms2024`. The information will be downloaded in JSON format.

Key Features
------------

- **Retrieve nomenclature information from WoRMS database.** Users can access the nomenclature details of a given taxon stored in the WoRMS database.
- **Obtain taxon distribution.** Users can obtain the distribution of a given taxon.


Retrieve nomenclature from WoRMS
--------------------------------

In this example, we download the nomenclature from WoRMS for a list of taxa by setting the ``bulk`` parameter to *True*. Additionally, we set the parameter ``marine_only`` to restrict the search only for species belong the marine environment. This function utilizes the WoRMS ChecklistBankAPI endpoint `rest/AphiaRecordByAphiaID`_.

.. _rest/AphiaRecordByAphiaID: https://www.marinespecies.org/rest/


.. note::

    The taxonomy list should be compiled using only the taxon names, excluding any authorship information.


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import WORMS

    # List of taxa
    taxa = ['Pinna nobilis', 'Delphinus delphis', 'Plerogyra sinuosa']

    # Start the download
    bdp = Biodumpy([WORMS(bulk=True, marine_only=True)])
    bdp.start(taxa, output_path='./biodumpy/downloads/{date}/{module}/{name}')


Retrieve distribution from WoRMS
--------------------------------

In the following example, we download the nomenclature and distribution data for the taxa. To include distribution information users can set the parameter ``distribution`` to *True*.

.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import WORMS

    # List of taxa
    taxa = ['Pinna nobilis', 'Delphinus delphis', 'Plerogyra sinuosa']

    # Start the download
    bdp = Biodumpy([WORMS(bulk=False, marine_only=False, distribution=True)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}_distribution/{name}')


Reference link/s
----------------

`WoRMS`_

.. _WoRMS: https://www.marinespecies.org/
