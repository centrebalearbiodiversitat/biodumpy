iNaturalist Module
==================

.. _iNat_module:


Overview
--------

The ``iNaturalist`` module allows users to easily retrieve photos from iNaturalist (`iNaturalist`_) database :cite:inaturalist2024. The information is downloaded in JSON format.


Key Features
------------

- **Retrieve photos from iNaturalist database.** Users can download the photo link from iNaturalist database.


Retrieve photo link from iNaturalist
------------------------------------

In this example, we download the information from iNaturalist setting the parameter ``bulk`` to *True*. This function is based on the iNaturalist v1 API's endpoint `v1/taxa`_.

.. _v1/taxa: https://api.inaturalist.org/v1/taxa

.. note::

    The taxonomy list should be compiled using only the taxon names, excluding any authorship information.


.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import INaturalist
    # List of taxa
    taxa = [
        'Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis',
        'Anax imperator', 'Bufo roseus', 'Stollia betae'
    ]
    # Start the download
    bdp = Biodumpy([INaturalist(bulk=True)])
    bdp.start(taxa, output_path='./biodumpy/downloads/{date}/{module}/{name}')


To view the photo, users can append the 'image_id' value at the end of the following link: https://inaturalist-open-data.s3.amazonaws.com/photos/ . For example: https://inaturalist-open-data.s3.amazonaws.com/photos/34826202/medium.jpg

Photos can only be downloaded if they have one of the valid licenses listed below. If an iNaturalist photo has a license other than those specified, it cannot be downloaded.
Please carefully check the photo's license before using it.

A detailed list of the available licenses can be found here:

- **CC0** (Public Domain Dedication): No rights reserved. The creator waives all copyright, allowing anyone to use the work for any purpose without permission.
- **CC BY** (Attribution): Others can distribute, remix, adapt, and build upon the work, even commercially, as long as they give the appropriate credit to the creator.
- **CC BY-NC** (Attribution-NonCommercial): Others can remix, adapt, and build upon the work non-commercially. While new works must also acknowledge the creator, they don’t have to be licensed on the same terms.
- **CC BY-NC-ND** (Attribution-NonCommercial-NoDerivs): Others can download and share the work, but can’t change it or use it commercially, and must give credit to the creator.
- **CC BY-SA** (Attribution-ShareAlike): Others can remix, adapt, and build upon the work, even commercially, but must credit the creator and license their new creations under the same terms.
- **CC BY-ND** (Attribution-NoDerivs): Others can share the work, but they can't alter it or use it commercially, and they must credit the creator.
- **CC BY-NC-SA** (Attribution-NonCommercial-ShareAlike): Others can remix, adapt, and build upon the work non-commercially, as long as they give credit and license their new creations under the same terms.


Reference link/s
----------------

`iNaturalist`_

.. _iNaturalist: https://www.inaturalist.org/