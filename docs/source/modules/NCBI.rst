NCBI Module
===========

.. _NCBI_module:

Overview
--------

The ``NCBI`` module allows users to easily retrieve data information from the the National Center for Biotechnology
Information (`NCBI`_) database. The information can be downloaded in JSON or FASTA format.


Key Features
------------

- **Retrieve information from NCBI database.** Users can download the information stored into the NCBI database.
- **Retrieve genetic information from NCBI database.** Users can download the genetic information in FASTA format.


Retrieve comprehensive metadata from NCBI
-----------------------------------------

In this example, we download the information from NCBI setting the parameter ``bulk`` to *True*. We download the data
from the "nucleotide" database in GeneBank format. Do not underestimate the parameter ``query_type`` since it defines
the type of query search. This function is based on biopython `Entrez`_ module.

.. _Entrez: https://biopython.org/docs/1.75/api/Bio.Entrez.html

.. note::

    The taxonomy list should be compiled using only the taxon names, excluding any authorship information.


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import NCBI

    taxa = ['Alytes muletensis', 'Hyla meridionalis', 'Anax imperator', 'Bufo roseus', 'Stollia betae']

    # Start the download
    bdp = Biodumpy([NCBI(bulk=False, mail="hola@quetal.com", db="nucleotide", rettype="gb", query_type='[Organism]')])
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')


Users can refine their search by adjusting the ``query_type`` parameter. For instance, if you want to download sequences
related to the cytochrome c oxidase marker (COI), you can set the ``query_type`` to '[Organism] AND "COI" [Gene]'.
This allows you to combine multiple search criteria to better target the specific data you need.

.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import NCBI

    taxa = ['Anax imperator']

    # Start the download
    bdp = Biodumpy([NCBI(bulk=False, mail="hola@quetal.com", db="nucleotide",
        rettype="gb", query_type='[Organism] AND "COI" [Gene]')])
    bdp.start(taxa, output_path='./downloads/{date}/{module}_gene/{name}')


Download NCBI a summary of metadata
-----------------------------------

Users can also obtain a summary of metadata by setting the ``summary`` parameter to *True*.
When enabled, the resulting JSON will include the following details:

- **Id**: A numerical identifier (GI Number) that used to be assigned to each sequence version (e.g., "345678912").
- **Caption**: A unique identifier (accession number) assigned to a sequence when it is submitted to GenBank (e.g., "NM_001256789").
- **Title**: A short description or title of the sequence, often including information about the gene, organism, and type of sequence.
- **Length**: The length of the sequence in base pairs (for nucleotide sequences) or amino acids (for protein sequences).
- **query**: The original search term or query string used to retrieve this result.

.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import NCBI

    taxa = ['Alytes muletensis', 'Hyla meridionalis', 'Anax imperator', 'Bufo roseus', 'Stollia betae']

    # Start the download
    bdp = Biodumpy([NCBI(bulk=False, mail="hola@quetal.com", db="nucleotide",
        rettype="gb", query_type='[Organism]', summary=True)])
    bdp.start(taxa, output_path='./downloads/{date}/{module}_summary/{name}')


Downloading data in FASTA format
--------------------------------

This function also provides a boolean ``fasta`` parameter to download the file in FASTA format. Following the general
structure of the ``biodumpy`` package, sequences can be downloaded for individual organisms or in bulk. Below is an
example demonstrating how to download FASTA files.

.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import NCBI

    taxa = ['Alytes muletensis', 'Hyla meridionalis', 'Anax imperator', 'Bufo roseus', 'Stollia betae']

    # Start the download
    bdp = Biodumpy([NCBI(bulk=False, mail="hola@quetal.com", db="nucleotide", rettype="fasta",
        query_type='[Organism]', summary=True, output_format='fasta')])
    bdp.start(taxa, output_path='./downloads/{date}/{module}_fasta/{name}')



Downloading using the NCBI accession number
-------------------------------------------

If needed, users can download data using a list of NCBI accession numbers as input by setting the ``by_id`` parameter to
*True*. In this case, the ``query_type`` parameter must be set to ``None`` or an empty string (``""``).
It is possible combine this approach also to download summary JSON or FASTA files.

.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import NCBI

    acc_numb = ["OQ507551", "OQ507547", "OQ507535", "OQ507524", "MW490509"]

    # Start the download
    bdp = Biodumpy([NCBI(bulk=True, mail="hola@quetal.com", db="nucleotide", rettype="gb", query_type = None, by_id=True)])
    bdp.start(acc_numb, output_path='./downloads/{date}/{module}_acc_num/{name}')


Reference link
--------------

`NCBI`_

.. _NCBI: https://www.ncbi.nlm.nih.gov
