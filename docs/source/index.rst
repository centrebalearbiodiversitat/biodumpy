.. image:: static/Biodumpy_logo.png
   :alt: biodumpy logo
   :width: 300px
   :height: 300px
   :align: center


Welcome to ``biodumpy``: A Comprehensive Biological Data Downloader
===================================================================

Overview
--------
In recent years, public biodiversity platforms and their associated datasets have grown significantly, driven by advancements in research, institutional efforts, expanded data storage capabilities, and the availability of powerful computational tools. These developments have provided unprecedented access to ecological and biological data, covering extensive geographic regions, long time periods, and a wide array of taxonomic groups. Such resources have become essential in ecological research, enabling scientists to undertake more thorough analyses and explore hypotheses that were previously unfeasible due to data constraints. These constraints include issues such as inconsistent data quality, low data quantity, and the heterogeneity of sources.

As these databases have expanded, so too has the number of programming libraries aimed at facilitating data access and interaction, making data retrieval more straightforward. However, most of these tools have been designed to work with a single database, posing difficulties for researchers who need to integrate information from multiple sources.

To overcome this limitation, we developed ``biodumpy``, a Python library that simplifies the retrieval, management, and integration of biological data across various public databases. ``biodumpy`` grants users access to a broad range of up-to-date datasets, including genetic, distributional, taxonomic, and bibliographic information. Its modular design enables efficient data retrieval tailored to specific taxa, with support for processing multiple modules concurrently.

.. _`Python`: https://www.python.org/downloads/

.. note::

   This project is under active development.

Key Features
------------

``biodumpy`` offers dedicated modules for each supported database. Each module comes with specific parameters tailored to retrieve information from its respective source. Explore the :doc:`modules` section to learn about the currently supported modules.


.. toctree::
   :maxdepth: 1
   :caption: Contents

   usage
   modules
   functions
   useful_code
   To R
   bibliography


Contribution
------------

``biodumpy`` is an open-source project, and contributions are welcome! If you have ideas for new features, bug fixes, or improvements, please submit an issue or pull request on our GitHub repository or contact our support `here <mailto:tommaso.cancellario@gmail.com?subject=biodumpy_support>`_.


License
-------

``biodumpy`` is licensed under the **GNU AGPLv3** License for its software components. Additionally, any creative works associated with this project—such as documentation, visual assets, or other non-code materials—are licensed under the Creative Commons Attribution (CC BY 4.0) license. See the `LICENSE`_ file for full details.

.. _`LICENSE`: https://github.com/centrebalearbiodiversitat/biodumpy/blob/master/LICENSE

Disclaimer
----------
The data retrieved and downloaded using this package is sourced from external databases. We do not take responsibility for the accuracy, completeness, or currency of the data. Users are advised to verify the information independently. By using this package, you agree that the authors and contributors are not liable for any errors, omissions, or potential consequences arising from the use of the data.

If you encounter any bugs or issues using the package, please contact the developers for support.


Citation
--------
Please cite the following paper if you use ``biodumpy``: 
   
   APA: 
      Cancellario, T., Golomb Durán , T., Far, A. J., Roldán, A., & Capa, M. (2026). Biodumpy: A comprehensive biological data downloader. Biodiversity Informatics, 20(1). https://doi.org/10.17161/bi.v20i1.24725

   BibTeX: 
      @article{Cancellario_Golomb Durán_Far_Roldán_Capa_2026, title={Biodumpy: A comprehensive biological data downloader}, volume={20}, url={https://journals.ku.edu/jbi/article/view/24725}, DOI={10.17161/bi.v20i1.24725}, abstractNote={In recent years, the expansion of public biodiversity platforms and associated datasets has greatly improved access to ecological and biological information. These resources now cover vast geographic areas, extended temporal scales, and diverse taxonomic groups, becoming essential for ecological studies by enabling more comprehensive analyses and novel hypotheses testing. Concurrently, the development of programming packages has facilitated data access and interaction, optimizing their retrieval processes. However, most existing tools are limited to specific databases, posing challenges for studies requiring smooth data integration from multiple sources. The growing availability of biodiversity records highlight the urgent need for robust tools to efficiently download, process, and analyse, ecological and biological information. To address this limitation, we introduce biodumpy, a new Python package developed for the retrieval, management, and integration of biological data from several public databases. Biodumpy provides access to up-to-date and comprehensive datasets spanning genetic, geographic, taxonomic, and bibliographic sources. It includes specialized modules for efficient data retrieval across taxonomic lists, with the possibility to process multiple modules simultaneously. By integrating diverse data sources, biodumpy enhances data acquisition, providing researchers with a powerful framework for comprehensive analyses and supporting ecological research to tackle complex environmental challenges.}, number={1}, journal={Biodiversity Informatics}, author={Cancellario, Tommaso and Golomb Durán , Tomas and Far, Antoni Josep and Roldán, Alejandro and Capa, Maria}, year={2026}, month={Mar.} }

Acknowledgments
---------------

This package has been partially sponsored and promoted by the Comunitat Autonoma de les Illes Balears through the Conselleria d'Educació i Universitats and by the European Union- Next Generation EU/PRTR-C17.I1.
