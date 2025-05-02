From Python to R
======================

Overview
--------

We defined ``biodumpy`` as "a powerful and versatile Python package designed to simplify the process of retrieving biological information from several public databases." However, there is another programming language that, alongside Python, shares the spotlight in the realm of biological software: R.

In this guide, we include examples of using ``biodumpy`` in R to create a more comprehensive resource for users. To facilitate this integration, we utilize the R package ``reticulate`` :cite:`ushey2024`. This package serves as a powerful bridge between R and Python, enabling seamless communication between the two languages.
With ``reticulate``, users can call Python code directly from R, access a wide array of Python libraries, and effortlessly exchange data between R and Python formats.

By incorporating ``biodumpy`` within the R environment, users can leverage the strengths of both programming languages, utilizing Python’s advanced capabilities alongside R’s rich statistical analysis and visualization tools. This not only enhances the flexibility of data analysis workflows but also broadens the range of applications available to researchers in the field of bioinformatics.


Introduction to the ``reticulate`` workflow
-------------------------------------------

Before to start with ``biodumpy`` we need to understand some of the main functions provided by ``reticulate``. While the workflow described below might be obvious to Python users, it could be new for R users, as it differs mainly in the initial steps of setting up a new project.

More information about ``reticulate`` are available at `reticulate`_ webpage.

.. _reticulate: https://rstudio.github.io/reticulate/index.html


Getting started with ``reticulate``
-----------------------------------

Users can install ``reticulate`` directly from CRAN as follows:

.. code-block:: R

	# Install the reticulate pack
	install.packages("reticulate", dependencies=TRUE)


Once the package is installed, users can set up a specific *virtual environment*. Likely, this step is uncommon for R users, but it's important to understand it properly. Like R, Python has a vast number of packages outside its core that can add new functionalities beyond the standard Python installation. However, only one version of a package can be installed at a time, which can be problematic if you're working on multiple projects that require different package versions, as they may conflict with other dependencies.
To solve this inconvenience, Python offers the possibility to create a *virtual environment* to manage the packages and their dependencies for each project independently.

By default, ``reticulate`` use an isolated Python virtual environment named "r-reticulate". However, users can modify the virtual environment using the command ``use_virtualenv()``.

.. code-block:: R

	# Load reticulate package
	library(reticulate)

	# Create a new environment
	virtualenv_create("myenv") # Substitute myenv with your environmental name

	# Set a specific virtualenv and install the biodumpy pack
	# Once users have created a virtual environment for the first time, they can activate it using use_virtualenv()
	use_virtualenv("myenv")
	virtualenv_install("myenv", "biodumpy")

If users copied the above code and it did not return any errors, then the installation of ``biodumpy`` in the virtual environment named "myenv" was successful. Now it is possible to use ``biodumpy`` into the R environment.

In the following examples, we will use only a few functionalities of ``biodumpy``. For a more detailed explanation and to see how to use additional parameters for the functions, please refer to the section: :doc:`modules` or check the function *help*.

Below, we provide two examples of using biodumpy in R:

- **Example n. 1**: Using a single module, specifically the NCBI module.
- **Example n. 2**: Using a list of modules, specifically the BOLD and COL modules.

.. code-block:: R

	# Import the necessary modules from biodumpy
	biodumpy <- import("biodumpy")
	inputs <- import("biodumpy.inputs")

	# Define the taxa vector
	taxa <- list("Alytes muletensis", "Hyla meridionalis")

	#-----------#
	# Example 1 #
	#-----------#

	# Create an instance to use the NCBI module
	ncbi <- inputs$NCBI(bulk = FALSE, mail = "hola@quetal.com", db = "nucleotide", query_type = '[Organism]')

	# Create an instance of Biodumpy with the NCBI module
	bdp <- biodumpy$Biodumpy(list(ncbi))

	# Start the process with the specified taxa and output path
	bdp$start(taxa, output_path = "./downloads_ex1/{date}/{module}/{name}")

	#-----------#
	# Example 2 #
	#-----------#

	# Create the instances of BOLD and COL module
	bold <- inputs$BOLD(bulk = FALSE, summary = TRUE)
	CoL <- inputs$COL(bulk = FALSE)

	# Create an instance of Biodumpy with a list of modules
	bdp <- biodumpy$Biodumpy(list(bold, CoL))

	# Start the process with the specified taxa and output path
	bdp$start(taxa, output_path = "./downloads_ex2/{date}/{module}/{name}")
