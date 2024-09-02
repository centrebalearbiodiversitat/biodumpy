BOLD Module
===========

.. _BOLD_module:


Overview
--------

The ``BOLD`` module allows users to easily retrieve data information from the Barcode of Life Data System (`BOLD`_)
database. The information is downloaded in JSON or FASTA format.

.. _BOLD: https://www.boldsystems.org/

Key Features
------------

- **Retrieve information from BOLD database.** Users can download the information stored into the BOLD database.
- **Retrieve genetic information from BOLD database.** Users can download the genetic information in FASTA format.

Retrieve comprehensive metadata from BOLD
-----------------------------------------

In this example, we download the information from BOLD setting the parameter ``bulk`` to *True*.
This function is based on the BOLD v4 API's endpoints `API_Public/combined`_ and `API_Public/sequence`_.

.. _API_Public/combined: http://v4.boldsystems.org/index.php/API_Public/combined?
.. _API_Public/sequence: http://v4.boldsystems.org/index.php/API_Public/sequence?

.. note::

    The taxonomy list should be compiled using only the taxon names, excluding any authorship information.


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import BOLD

    # Taxa list
    taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis', 'Anax imperator']

    # Set the module and start the download
    bdp = Biodumpy([BOLD(bulk=True, summary=False)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')


The previous method downloads the entire set of data for each record from BOLD. However, users can also download a
summarized version by setting the ``summary`` parameter to *True*. This option provides a more concise and manageable
set of information. The fields of the result file are described below:

- record_id: The unique identifier for the BOLD record.
- processid: The process ID associated with the BOLD record.
- bin_uri: The BIN (Barcode Index Number) URI.
- taxon: The name of the lower taxon extracted from the taxonomy information.
- country: The country where the collection event took place.
- province_state: The province or state of the collection event.
- region: The region of the collection event.
- lat: The latitude of the collection event.
- lon: The longitude of the collection event.
- markercode: The marker code from the sequences data.
- genbank_accession: The GenBank accession number from the sequences data.

This function also provides a boolean ``fasta`` parameter to download the file in FASTA format.
Following the general structure of the ``biodumpy`` package, sequences can be downloaded for individual organisms or in
bulk. Below is an example demonstrating how to download FASTA files.

.. note::

    Be sure to set the parameters ``fasta=True`` and ``output_format='fasta'``. Otherwise, the function will be blocked.

.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import BOLD

    # Taxa list
    taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis', 'Anax imperator']
    # Set the module and start the download
    bdp = Biodumpy([BOLD(bulk=True, fasta=True, output_format='fasta')])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')



Reference link/s
----------------

`Barcode of Life Data Systems`_

.. _Barcode of Life Data Systems: https://boldsystems.org/