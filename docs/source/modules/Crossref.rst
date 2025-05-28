Crossref Module
===============

.. _Crossref_module:


Overview
--------

The ``Crossref`` module allows users to easily retrieve scientific bibliographic metadata from Crossref database :cite:`crossref2024`. By providing a list of Digital Object Identifier (DOI), users can access to bibliographic data.

.. toggle:: Click to expand

    JSON


Key Features
------------

- **Retrieve scientific bibliographic metadata**. Access to bibliographic metadata stored in Crossref.


Retrieve comprehensive metadata from Crossref
---------------------------------------------

This example demonstrates how users can download bibliographic information from Crossref using a list of DOIs as input. The function relies on the Crossref API's `works`_ endpoint.


.. _works: https://api.crossref.org/swagger-ui/index.html


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import Crossref

    # Create a list of doi
    doi = ["10.1038/s44185-022-00001-3", "10.1111/gcb.17059", "10.1016/j.ecoinf.2024.102629"]

    # Set the Biodumpy functions with the specific parameters
    bdp = Biodumpy([Crossref(bulk=True)])
    bdp.start(doi, output_path='./downloads/{date}/{module}/{name}')


The previous method downloads the entire set of data for each record from Crossref. However, users can also download a summarized version by setting the ``summary`` parameter to *True*. This option provides a more concise and manageable set of information. The fields of the result file are described below:

- **publisher**: The name of the publishing entity responsible for releasing the publication.
- **container-title**: The title of the journal or book in which the research is published.
- **DOI**: The Digital Object Identifier assigned to the publication.
- **type**: The type of the publication, such as article, book chapter, report, etc.
- **language**: The language in which the publication is written.
- **URL**: A direct link to the publication.
- **published**: The date when the research was published.
- **title**: The title of the publication.
- **author**: The names of the authors who contributed to the research along with their main academic information.
- **abstract**: The publication abstract (if available).

Example of data filtering
-------------------------


Reference link/s
----------------

`Crossref`_

.. _Crossref: https://www.crossref.org/