# biodumpy: A Comprehensive Biological Data Downloader

## Overview
**biodumpy** is a powerful and versatile Python package designed to simplify the process of retrieving biological data 
from several public databases. 
With **biodumpy**, researchers can easily download and manage data from multiple sources, ensuring they have access to 
the most up-to-date and comprehensive biological information available.


## Key Features

### Multi-Database Support 
**biodumpy** provides seamless integration with several biological databases, including:

- [NCBI (National Center for Biotechnology Information)](https://www.ncbi.nlm.nih.gov)
- [BOLD (Barcode of Life Data Systems)](https://boldsystems.org/)
- [GBIF (Global Biodiversity Information Facility)](https://www.gbif.org/)
- [CoL (Catalogue of Life)](https://catalogueoflife.org/)


## Installation
```bash
pip install biodumpy
```


## Use NCBI module.
```bash
from biodumpy import Biodumpy
from biodumpy.inputs import NCBI

bdp = Biodumpy([NCBI(mail="hola_ncbi@quetal.com", step=100, max_bp=1000, rettype='gb', output_format='json', bulk=False)])

# List of taxa
taxa = ['Alytes muletensis', 'Anax imperator']
```


### Download NCBI metadata by Taxon name.
Before running the function to download the data, we need to prepare the data by creating a list of dictionaries. 
Each dictionary should contain the indices **name** and **query**, indicating the species name and the corresponding 
NCBI query, respectively.
```bash
 result_list = []

# Create a dictionary with 'name' and 'query' from corresponding indices
 for taxon in taxa:
     element_dict = {
         'name': taxon,
         'query': f'{taxon}[Organism]'
     }
     result_list.append(element_dict)

 bdp.start(result_list, output_path="downloads/{date}/{name}_{module}")
```


### Download NCBI metadata by taxon ID.
```bash
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
```


### Retrieve NCBI accession number from NCBI json file.
```bash
import json

with open('YOUR_PATH/.json', 'r') as f:
    data = json.load(f)

accession_number = []
for i in range(len(data)):
    accession_number.append(data[i].get('name', ''))

print(accession_number)
```


### Download NCBI fasta by Taxon Name.
To download a FASTA file from NCBI, we need to change the parameter *rettype* in the Biopython function. 
Additionally, it is useful to change the name of the module to {module}_fasta.
```bash
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
```


### Download "bulk" output.
"Bulk download" refers to the process of downloading a large volume of data files in a single operation, consolidating 
them together. This is often done to facilitate data analysis and to have a single file containing broad information. 
However, this process can create a massive resulting file. Therefore, we suggest using this function carefully.
```bash
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
```






## Documentation and Support
For detailed documentation, tutorials, and support, please visit the **biodumpy** GitHub section Tutorial or contact 
our support team at XXX@biodumpy.com.


## Contribution
**biodumpy** is an open-source project, and contributions are welcome! 
If you have ideas for new features, bug fixes, or improvements, please submit an issue or pull request on our GitHub repository.


## License
**biodumpy** is licensed under the GNU GENERAL PUBLIC LICENSE. See the LICENSE file for more details.


## Acknowlegments
The project was supported by MCIN with funding from European Union—NextGenerationEU (PRTR-C17.I1) and 
the Government of the Balearic Islands.

<hr>
<div style="display: flex; justify-content: center">
<img src='/www/logo_cbb.png' alt='logo_cbb' width='200'>
</div>


