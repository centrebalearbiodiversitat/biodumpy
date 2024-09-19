<img src="./docs/source/Biodumpy_logo.png" alt="Project Logo" width="200">

# biodumpy: A Comprehensive Biological Data Downloader

![PyPI - Version](https://img.shields.io/pypi/v/biodumpy)
![PyPI - Status](https://img.shields.io/pypi/status/biodumpy)
![PyPI - License](https://img.shields.io/pypi/l/biodumpy)
![PyPI - Downloads](https://img.shields.io/pypi/dm/biodumpy)



## Overview
``biodumpy`` is a powerful and versatile Python package designed to simplify the process of retrieving biological information 
from several public databases. 
With ``biodumpy``, researchers can easily download and manage data from multiple sources, ensuring access to the most 
up to date and comprehensive biological information available.

> **Note:** This package is currently under development.


## Key Features
``biodumpy`` offers dedicated modules for each supported database, with each module featuring functions specifically 
designed for retrieving information from its respective source. The modules implemented so far are:

- BOLD
- COL
- GBIF
- iNaturalist
- IUCN
- NCBI
- OBIS
- ZooBank

This list can be expanded, thus suggestions and feedback are greatly appreciated.


## Main functionalities and workflow
Before using ``biodumpy``, users need to install the package in their Python environment with the following command:

```
pip install biodumpy
```

### Usage
To simplify the use of ``biodumpy``, we create a general structure common among the modules:

1) **Load the package.** Import ``biodumpy`` into your Python environment.
2) **Load the desired modules.** Import one or more specific modules needed to retrieve the data.
3) **Set up the configuration of one or more modules.** Configure the ``biodumpy`` function/s with the required parameters.
4) **Start the download.** Execute the function to begin retrieving the data.

Here, we provide two examples illustrating the general structure of a ``biodumpy`` script:

In detail, we described:
- **Single Module Example**: This example demonstrates how to use a single ``biodumpy`` module (for example, GBIF).
- **Multiple Modules Example**: This example shows how to use multiple ``biodumpy`` modules (for example, GBIF and IUCN).

**Example N.1**

``` python

    # Import biodumpy package
    from biodumpy import Biodumpy

    # Import GBIF module
    from biodumpy.inputs import GBIF

    # Create a list of taxa
    taxa = [
        'Alytes muletensis (Sanchíz & Adrover, 1979)', 
        'Bufotes viridis (Laurenti, 1768)',
        'Hyla meridionalis Boettger, 1874', 
        'Anax imperator Leach, 1815'
    ]

    # Set the Biodumpy function with the specific parameters
    bdp = Biodumpy([GBIF(bulk=False, accepted_only=True)])

    # Start the download
    bdp.start(taxa, output_path='YOUR_OUTPUT_PATH/downloads/{date}/{module}/{name}')
```

**Example N.2**

``` python

    # Import biodumpy package
    from biodumpy import Biodumpy

    # Import GBIF and IUCN modules
    from biodumpy.inputs import GBIF, IUCN

    api_key = 'YOUR_IUCN_API_KEY'

    # Create a list of taxa
    taxa = [
        'Alytes muletensis', 
        'Bufotes viridis', 
        'Hyla meridionalis', 
        'Anax imperator'
    ]

    # Set the Biodumpy functions with the specific parameters
    bdp = Biodumpy([GBIF(bulk=False, accepted_only=True),
                    IUCN(api_key=api_key, bulk=True, region=['global'])])

    # Start the download
    bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')
```

## Documentation and Support
For detailed documentation and tutorials, please visit the ``biodumpy`` Read the Docs documentation.


## Contribution
``biodumpy`` is an open-source project, and contributions are welcome! 
If you have ideas for new features, bug fixes, or improvements, please submit an issue or pull request in our GitHub 
repository or contact with the support team at [t.cancellario@uib.eu](mailto:t.cancellario@uib.eu).


## License
``biodumpy`` is licensed under the GNU GENERAL PUBLIC LICENSE. See the LICENSE file for more details.


## Acknowledgments
The project was supported by MCIN with funding from the European Union—NextGenerationEU (PRTR-C17.I1) and 
the Government of the Balearic Islands.



<hr>
<div style="display: flex; justify-content: center">
<img src='./docs/source/logo_cbb.png' alt='logo_cbb' width='200'>
</div>
