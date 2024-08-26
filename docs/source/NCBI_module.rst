NCBI Module
===========

.. _NCBI_module:

.. code-block:: python

    from biodumpy import Biodumpy
    from biodumpy.inputs import NCBI

    bdp = Biodumpy([NCBI(mail="hola_ncbi@quetal.com", step=100, max_bp=1000, rettype='gb', output_format='json', bulk=False)])

    # List of taxa
    taxa = ['Alytes muletensis', 'Anax imperator']


Download NCBI metadata by Taxon name
------------------------------------

Before running the function to download the data, we need to prepare the data by creating a list of dictionaries. 
Each dictionary should contain the indices ``name`` and ``query``, indicating the species name and the corresponding 
NCBI query, respectively.

.. code-block:: python

    result_list = []

    # Create a dictionary with 'name' and 'query' from corresponding indices
    for taxon in taxa:
        element_dict = {
            'name': taxon,
            'query': f'{taxon}[Organism]'
        }
        result_list.append(element_dict)

    bdp.start(result_list, output_path="downloads/{date}/{name}_{module}")


Download NCBI metadata by taxon ID
----------------------------------

.. code-block:: python
    
    taxon_ids = []
    for taxon in taxa:
        taxon_ids.append(NCBI.taxonomy_id(taxon, lineage=False))
        print(taxon_ids[-1])

    result_list = []
    for taxon_id in taxon_ids:
        element_dict = {
            'name': taxon_id['ScientificName'],
            'query': f'txid{taxon_id["TaxId"]}[Organism]'
        }
        # Append the dictionary to the result_list
        result_list.append(element_dict)
        
    bdp.start(result_list, output_path="downloads/{date}/{name}_{module}")



Retrieve NCBI accession number from NCBI json file
--------------------------------------------------

.. code-block:: python

    import json

    with open('YOUR_PATH/.json', 'r') as f:
        data = json.load(f)

    accession_number = []
    for i in range(len(data)):
        accession_number.append(data[i].get('name', ''))

    print(accession_number)


Download NCBI fasta by Taxon Name
---------------------------------

To download a FASTA file from NCBI, we need to change the parameter *rettype* in the Biopython function. 
Additionally, it is useful to change the name of the module to {module}_fasta.

.. code-block:: python

    bdp = Biodumpy([NCBI(mail="hola_ncbi@quetal.com", step=100, max_bp=1000, rettype='fasta', output_format='fasta', bulk=False)])

    result_list = []

    # Create a dictionary with 'name' and 'query' from corresponding indices
    for taxon in taxa:
        element_dict = {
            'name': taxon,
            'query': f'{taxon}[Organism]'
        }
        result_list.append (element_dict)

    bdp.start (result_list, output_path="downloads/{date}/{module}_fasta/{name}")


Download "bulk" output
----------------------

"Bulk download" refers to the process of downloading a large volume of data files in a single operation, consolidating 
them together. This is often done to facilitate data analysis and to have a single file containing broad information. 
However, this process can create a massive resulting file. Therefore, we suggest using this function carefully.

.. code-block:: python

    bdp = Biodumpy ([NCBI(mail="hola_ncbi@quetal.com", step=100, max_bp=1000, rettype='gb', output_format='json', bulk=True)])

    # List of taxa
    taxa = ['Alytes muletensis', 'Anax imperator']

    result_list = []
    # Create a dictionary with 'name' and 'query' from corresponding indices
    for taxon in taxa:
        element_dict = {
            'name': taxon,
            'query': f'{taxon}[Organism]'
        }
        result_list.append (element_dict)

    bdp.start (result_list, output_path="downloads/{date}/{module}/{name}")


Reference link
--------------

`National Center for Biotechnology Information`_

.. _National Center for Biotechnology Information: https://www.ncbi.nlm.nih.gov