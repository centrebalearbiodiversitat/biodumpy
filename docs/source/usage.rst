Main functionalities and workflow
=================================

.. _installation:

Before using **biodumpy**, users need to install the package in their Python environment with the following command:

.. code-block:: console

   (.venv) $ pip install biodumpy


Usage
^^^^^

To simplify the use of **biodumpy**, we create a general structure common among the modules:

1) Load the package: Import **biodumpy** into your Python environment.
2) Load the desired module: Import one or more specific modules needed to retrieve the data.
3) Set up the function: Configure the **biodumpy** function with the required parameters.
4) Start the download: Execute the function to begin retrieving the data.

Here we show an example resuming the general structure. In this case we use the GBIF module.

.. code-block:: python

   # Import biodumpy pachage
   from biodumpy import Biodumpy

   # Import GBIF module
   from biodumpy.inputs import GBIF 

   # Create a list of taxa
   taxa = ['Alytes muletensis (Sanchíz & Adrover, 1979)', 'Bufotes viridis (Laurenti, 1768)', 'Hyla meridionalis Boettger, 1874', 'Anax imperator Leach, 1815']

   # Set the Biodumpy function with the specific parameters
   bdp = Biodumpy([GBIF(bulk=False, accepted_only=True)])

   # Start the download
   bdp.start(taxa, output_path='YOUR_OUTPUT_PATH/downloads/{date}/{module}/{name}')


An important parameter common to all modules is ``bulk``. This parameter controls how the information is organized and 
saved thus users can customize how the data is organized according to their needs.

- If ``bulk`` is set to *True*, the information downloaded for each taxon is merged into a single file. 
  This option may be useful if the amount of the total data is limited and for consolidating data and simplifying file management.

- If ``bulk`` is set to *False*, the information for each taxon is saved in a separate file. 
  This option is beneficial for detailed analysis, when individual taxon files are required or when the amount of data for
  each taxon is large.

