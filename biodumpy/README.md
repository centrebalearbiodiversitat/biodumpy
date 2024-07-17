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

bdp = Biodumpy([
	NCBI(mail="hola_ncbi@quetal.com", step=100, max_bp=5000)
])

# List of taxa
taxa = ['Alytes muletensis', 'Anax imperator']
```


### Download NCBI metadata by Taxon Name.
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

 bdp.start(result_list, output_path="downloads2/{date}/{name}_{module}.json")
```


### Download NCBI metadata by taxon ID Name.
```bash
a=[]
for taxon in taxa:
    a.append(NCBI.taxonomy_id(taxon, lineage=False))
    print(a[-1])

result_list = []
for aa in a:
    element_dict = {
        'name': aa['ScientificName'],
        'query': f'txid{aa["TaxId"]}[Organism]'
    }
    # Append the dictionary to the result_list
    result_list.append(element_dict)
    
bdp.start(result_list, output_path="downloads2/{date}/{name}_{module}.json")
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


