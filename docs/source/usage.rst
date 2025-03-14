Main functionalities and workflow
=================================

.. _installation:

Before using ``biodumpy``, users need to install the package in their Python environment with the following command:

.. code-block:: console

   (.venv) $ pip install biodumpy


Usage
-----

To simplify the use of ``biodumpy``, we create a general structure common among all the modules:

1) **Load the package.** Import ``biodumpy`` into your Python environment.
2) **Load the desired modules.** Import one or more specific modules needed to retrieve the data.
3) **Set up the configuration of one or more modules.** Configure the ``biodumpy`` function/s with the required parameters.
4) **Start the download.** Execute the function to begin retrieving the data.

Here, we provide two examples illustrating the general structure of a ``biodumpy`` script:

In detail, we described:

- **Single Module Example**: This example demonstrates how to use a single ``biodumpy`` module (e.g., GBIF).

- **Multiple Modules Example**: This example shows how to use multiple ``biodumpy`` modules (e.g., GBIF and IUCN).

**Example N.1**

.. code-block:: python

    # Import biodumpy package
    from biodumpy import Biodumpy

    # Import GBIF module
    from biodumpy.inputs import GBIF

    # Create a list of taxa
    taxa = ['Alytes muletensis (Sanchíz & Adrover, 1979)', 'Bufotes viridis (Laurenti, 1768)',
            'Hyla meridionalis Boettger, 1874', 'Anax imperator Leach, 1815']

    # Set the Biodumpy function with the specific parameters
    bdp = Biodumpy([GBIF(bulk=False, accepted_only=True)])

    # Start the download
    bdp.download_data(taxa, output_path='YOUR_OUTPUT_PATH/downloads/{date}/{module}/{name}')


**Example N.2**

.. code-block:: python

    # Import biodumpy package
    from biodumpy import Biodumpy

    # Import GBIF and IUCN modules
    from biodumpy.inputs import GBIF, IUCN

    api_key = 'YOUR_IUCN_API_KEY'

    # Create a list of taxa
    taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis', 'Anax imperator']

    # Set the Biodumpy functions with the specific parameters
    bdp = Biodumpy([GBIF(bulk=False, accepted_only=True),
                    IUCN(api_key=api_key, bulk=True, region=['global'])])

    # Start the download
    bdp.download_data(taxa, output_path='./downloads/{date}/{module}/{name}')


The ``bulk`` parameter
~~~~~~~~~~~~~~~~~~~~~~

An important parameter common to all modules is ``bulk``. This parameter controls how the information is organized and 
saved thus users can customize how the data is organized according to their needs.

- If ``bulk`` is set to *True*, the information downloaded for each taxon is merged into a single file. 
  This option may be useful if the amount of the total data is limited and for consolidating data and simplifying file management.

- If ``bulk`` is set to *False*, the information for each taxon is saved in a separate file. 
  This option is useful for detailed analysis, when individual taxon files are required or when the amount of data for
  each taxon is large.

Save result location
~~~~~~~~~~~~~~~~~~~~

By default, ``biodumpy`` saves the resulting file in a folder named **download** into the working directory.
Inside this folder, it creates a subfolder with the current date, and within it, it creates another subfolder named with
the module name.